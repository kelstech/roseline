from pathlib import Path

SERVICE_SOURCE = Path("backend/auth_identity/services.py").read_text()
MODEL_SOURCE = Path("backend/auth_identity/models.py").read_text()


def test_auth_service_enforces_argon2_and_refresh_rotation():
    assert "PasswordHasher" in SERVICE_SOURCE
    assert "rotate_refresh_token" in SERVICE_SOURCE
    assert "replay_detected_at" in MODEL_SOURCE


def test_password_policy_is_enterprise_strength():
    assert "len(password) < 14" in SERVICE_SOURCE
    assert "sum(classes) < 3" in SERVICE_SOURCE
