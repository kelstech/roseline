from fastapi.testclient import TestClient
from app.main import create_app


def test_healthz():
    client = TestClient(create_app())
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "x-correlation-id" in response.headers


def test_auth_integration_placeholder():
    client = TestClient(create_app())
    response = client.get("/api/v1/system/auth-integration", headers={"Authorization": "Bearer placeholder"})
    assert response.status_code == 200
    assert response.json() == {"auth_enforced": False, "principal_detected": True}
