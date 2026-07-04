import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from .models import LoginAttempt, PasswordHistory, RefreshToken, Session, User, AccessToken


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


class AuthenticationError(Exception):
    pass


class AuthService:
    password_hasher = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16)
    access_minutes = 15
    refresh_days = 30
    max_failed_attempts = 5
    lockout_minutes = 15

    def _hash_token(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def hash_password(self, password: str) -> str:
        self.validate_password_policy(password)
        return self.password_hasher.hash(password)

    def validate_password_policy(self, password: str) -> None:
        classes = [any(c.islower() for c in password), any(c.isupper() for c in password), any(c.isdigit() for c in password), any(not c.isalnum() for c in password)]
        if len(password) < 14 or sum(classes) < 3:
            raise AuthenticationError("Password must be at least 14 characters and include three character classes.")

    @transaction.atomic
    def authenticate_password(self, username: str, password: str, ip_address: str, user_agent: str) -> TokenPair:
        user = User.objects.filter(username__iexact=username).first() or User.objects.filter(primary_email__iexact=username).first()
        if user is None:
            LoginAttempt.objects.create(username=username, success=False, failure_reason="unknown_user", ip_address=ip_address, user_agent=user_agent)
            raise AuthenticationError("Invalid credentials.")
        if user.locked_until and user.locked_until > timezone.now():
            LoginAttempt.objects.create(username=username, user=user, success=False, failure_reason="locked", ip_address=ip_address, user_agent=user_agent)
            raise AuthenticationError("Account is locked.")
        credential = user.credentials.filter(kind="password", revoked_at__isnull=True).order_by("-created_at").first()
        try:
            valid = credential is not None and self.password_hasher.verify(credential.secret_hash, password)
        except VerifyMismatchError:
            valid = False
        if not valid:
            LoginAttempt.objects.create(username=username, user=user, success=False, failure_reason="bad_password", ip_address=ip_address, user_agent=user_agent)
            failures = LoginAttempt.objects.filter(user=user, success=False, created_at__gte=timezone.now() - timedelta(minutes=15)).count()
            if failures >= self.max_failed_attempts:
                user.locked_until = timezone.now() + timedelta(minutes=self.lockout_minutes)
                user.status = User.Status.LOCKED
                user.save(update_fields=["locked_until", "status", "updated_at"])
            raise AuthenticationError("Invalid credentials.")
        LoginAttempt.objects.create(username=username, user=user, success=True, ip_address=ip_address, user_agent=user_agent)
        user.last_login_at = timezone.now()
        if user.status == User.Status.LOCKED:
            user.status = User.Status.ACTIVE
            user.locked_until = None
        user.save(update_fields=["last_login_at", "status", "locked_until", "updated_at"])
        return self.issue_token_pair(user=user, ip_address=ip_address, user_agent=user_agent, assurance_level="aal1")

    @transaction.atomic
    def issue_token_pair(self, user: User, ip_address: str, user_agent: str, assurance_level: str) -> TokenPair:
        now = timezone.now()
        session = Session.objects.create(user=user, ip_address=ip_address, user_agent=user_agent, expires_at=now + timedelta(days=self.refresh_days), assurance_level=assurance_level)
        access = AccessToken.objects.create(session=session, audience="ehis", scopes=["openid", "profile"], expires_at=now + timedelta(minutes=self.access_minutes))
        refresh_value = secrets.token_urlsafe(48)
        RefreshToken.objects.create(session=session, token_hash=self._hash_token(refresh_value), family_id=uuid.uuid4(), expires_at=now + timedelta(days=self.refresh_days))
        payload = {"sub": str(user.id), "sid": str(session.id), "jti": str(access.jti), "aud": "ehis", "iss": getattr(settings, "EHIS_ISSUER", "https://auth.ehis.local"), "iat": int(now.timestamp()), "exp": int(access.expires_at.timestamp()), "scope": "openid profile", "aal": assurance_level}
        token = jwt.encode(payload, getattr(settings, "EHIS_JWT_PRIVATE_KEY", "dev-secret-change-me"), algorithm=getattr(settings, "EHIS_JWT_ALG", "HS256"))
        return TokenPair(access_token=token, refresh_token=refresh_value, expires_in=self.access_minutes * 60)

    @transaction.atomic
    def rotate_refresh_token(self, refresh_token: str, ip_address: str, user_agent: str) -> TokenPair:
        token_hash = self._hash_token(refresh_token)
        stored = RefreshToken.objects.select_for_update().select_related("session", "session__user").filter(token_hash=token_hash).first()
        if stored is None or stored.revoked_at or stored.expires_at <= timezone.now():
            raise AuthenticationError("Invalid refresh token.")
        stored.rotated_at = timezone.now()
        stored.revoked_at = timezone.now()
        stored.save(update_fields=["rotated_at", "revoked_at", "updated_at"])
        return self.issue_token_pair(stored.session.user, ip_address, user_agent, stored.session.assurance_level)

    @transaction.atomic
    def change_password(self, user: User, new_password: str, actor_user_id=None, reason="user_change") -> None:
        password_hash = self.hash_password(new_password)
        active = user.credentials.filter(kind="password", revoked_at__isnull=True)
        for credential in active:
            PasswordHistory.objects.create(user=user, password_hash=credential.secret_hash, changed_by_user_id=actor_user_id, reason=reason)
            credential.revoked_at = timezone.now()
            credential.save(update_fields=["revoked_at", "updated_at"])
        user.credentials.create(kind="password", secret_hash=password_hash, expires_at=timezone.now() + timedelta(days=90))
