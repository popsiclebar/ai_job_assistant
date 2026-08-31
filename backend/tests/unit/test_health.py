"""Verifies the public health endpoint contract.
The test provides a fast signal that application wiring remains intact."""

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    """Confirm the running application reports its expected healthy status."""
    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
