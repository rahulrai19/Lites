from fastapi.testclient import TestClient
from app.core.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"
