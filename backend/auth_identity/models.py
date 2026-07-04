import uuid
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        LOCKED = "locked", "Locked"
        SUSPENDED = "suspended", "Suspended"
        DORMANT = "dormant", "Dormant"
        DEPROVISIONED = "deprovisioned", "Deprovisioned"

    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255)
    primary_email = models.EmailField(unique=True)
    primary_phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING, db_index=True)
    identity_type = models.CharField(max_length=64, db_index=True)
    home_facility_id = models.UUIDField(null=True, blank=True, db_index=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    locked_until = models.DateTimeField(null=True, blank=True)
    deprovisioned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["status", "identity_type"]), models.Index(fields=["home_facility_id", "status"])]


class Identity(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="identities")
    provider = models.CharField(max_length=120, db_index=True)
    subject = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    last_asserted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["provider", "subject"], name="uq_identity_provider_subject")]
        indexes = [models.Index(fields=["user", "provider"])]


class Credential(TimestampedModel):
    class Kind(models.TextChoices):
        PASSWORD = "password", "Password"
        PASSKEY = "passkey", "Passkey"
        CERTIFICATE = "certificate", "Certificate"
        API_KEY = "api_key", "API Key"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials")
    kind = models.CharField(max_length=32, choices=Kind.choices, db_index=True)
    secret_hash = models.TextField(blank=True)
    public_material = models.JSONField(default=dict, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "kind", "revoked_at"])]


class PasswordHistory(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_history")
    password_hash = models.TextField()
    changed_by_user_id = models.UUIDField(null=True, blank=True)
    reason = models.CharField(max_length=128)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]


class Session(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    device_id = models.UUIDField(null=True, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    last_seen_at = models.DateTimeField(default=timezone.now, db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    assurance_level = models.CharField(max_length=32, default="aal1")

    class Meta:
        indexes = [models.Index(fields=["user", "revoked_at", "expires_at"])]


class RefreshToken(TimestampedModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_hash = models.CharField(max_length=128, unique=True)
    family_id = models.UUIDField(db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    rotated_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    replay_detected_at = models.DateTimeField(null=True, blank=True)


class AccessToken(TimestampedModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="access_tokens")
    jti = models.UUIDField(unique=True, default=uuid.uuid4)
    audience = models.CharField(max_length=255)
    scopes = models.JSONField(default=list)
    expires_at = models.DateTimeField(db_index=True)
    revoked_at = models.DateTimeField(null=True, blank=True)


class LoginAttempt(TimestampedModel):
    username = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    success = models.BooleanField(default=False, db_index=True)
    failure_reason = models.CharField(max_length=128, blank=True)
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(blank=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["username", "success", "created_at"]), models.Index(fields=["ip_address", "success", "created_at"])]


class RegisteredDevice(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registered_devices")
    name = models.CharField(max_length=120)
    platform = models.CharField(max_length=64)
    fingerprint_hash = models.CharField(max_length=128, db_index=True)
    push_token_ref = models.CharField(max_length=255, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "fingerprint_hash"], name="uq_user_device_fingerprint")]


class TrustedDevice(TimestampedModel):
    device = models.ForeignKey(RegisteredDevice, on_delete=models.CASCADE, related_name="trust_records")
    trusted_until = models.DateTimeField(db_index=True)
    trust_token_hash = models.CharField(max_length=128, unique=True)
    revoked_at = models.DateTimeField(null=True, blank=True)


class AuthenticationMethod(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_methods")
    method = models.CharField(max_length=64, db_index=True)
    enabled = models.BooleanField(default=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(default=100)


class MFADevice(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mfa_devices")
    method = models.CharField(max_length=32, db_index=True)
    label = models.CharField(max_length=120)
    secret_ref = models.CharField(max_length=255, blank=True)
    phone_mask = models.CharField(max_length=32, blank=True)
    public_key = models.JSONField(default=dict, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)


class RecoveryCode(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recovery_codes")
    code_hash = models.CharField(max_length=128, unique=True)
    used_at = models.DateTimeField(null=True, blank=True)


class OAuthClient(TimestampedModel):
    client_id = models.CharField(max_length=120, unique=True)
    client_secret_hash = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    redirect_uris = models.JSONField(default=list)
    allowed_scopes = models.JSONField(default=list)
    grant_types = models.JSONField(default=list)
    pkce_required = models.BooleanField(default=True)
    active = models.BooleanField(default=True)


class APIClient(TimestampedModel):
    owner_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    key_hash = models.CharField(max_length=128, unique=True)
    scopes = models.JSONField(default=list)
    expires_at = models.DateTimeField(db_index=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)


class IdentityProvider(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    protocol = models.CharField(max_length=32)
    issuer = models.CharField(max_length=255, unique=True)
    metadata_url = models.URLField(blank=True)
    jwks_uri = models.URLField(blank=True)
    enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)


class AuditEvent(TimestampedModel):
    actor_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="audit_events")
    event_type = models.CharField(max_length=128, db_index=True)
    outcome = models.CharField(max_length=32, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    subject_user_id = models.UUIDField(null=True, blank=True, db_index=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["event_type", "created_at"]), models.Index(fields=["subject_user_id", "created_at"])]


class VerificationToken(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_tokens")
    channel = models.CharField(max_length=16, db_index=True)
    destination_hash = models.CharField(max_length=128)
    token_hash = models.CharField(max_length=128, unique=True)
    expires_at = models.DateTimeField(db_index=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
