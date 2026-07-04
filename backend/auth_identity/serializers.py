from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    device_fingerprint = serializers.CharField(required=False, allow_blank=True)


class TokenPairSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")
    expires_in = serializers.IntegerField()


class RefreshRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class MFAEnrollmentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=["totp", "sms", "email", "push", "webauthn"])
    label = serializers.CharField(max_length=120)


class MFAVerificationSerializer(serializers.Serializer):
    challenge_id = serializers.UUIDField()
    code = serializers.CharField(max_length=128, trim_whitespace=False)
    remember_device = serializers.BooleanField(default=False)


class PasswordResetRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    channel = serializers.ChoiceField(choices=["email", "sms"])


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    platform = serializers.CharField(max_length=64)
    fingerprint = serializers.CharField(max_length=512)
    push_token = serializers.CharField(required=False, allow_blank=True)
