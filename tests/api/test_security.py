from fastapi.testclient import TestClient

from dataset_gate.api.app import create_app
from dataset_gate.api.security import MAX_REQUEST_BYTES


def test_token_and_host_protection(tmp_path):
    with TestClient(create_app(tmp_path / "runs.db", token="test-secret")) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/api/v1/rules").status_code == 401
        assert (
            client.get("/api/v1/rules", headers={"Authorization": "Bearer wrong"}).status_code
            == 401
        )
        response = client.get("/api/v1/rules", headers={"Authorization": "Bearer test-secret"})
        assert (
            response.status_code == 200 and response.headers["x-content-type-options"] == "nosniff"
        )
        assert client.get("/health", headers={"Host": "attacker.example"}).status_code == 400


def test_body_limits_and_content_types(client):
    assert (
        client.post(
            "/api/v1/profile", content="{}", headers={"Content-Type": "text/plain"}
        ).status_code
        == 415
    )
    assert (
        client.post(
            "/api/v1/profile",
            content="{}",
            headers={
                "Content-Type": "application/json",
                "Content-Length": str(MAX_REQUEST_BYTES + 1),
            },
        ).status_code
        == 413
    )

    def chunks():
        for _ in range(7):
            yield b"x" * 1_000_000

    assert (
        client.post(
            "/api/v1/profile", content=chunks(), headers={"Content-Type": "application/json"}
        ).status_code
        == 413
    )
