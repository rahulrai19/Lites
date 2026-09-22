import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.api.server import app
from app.config.env import env
from app.core.exceptions import ProviderError

VALID_API_KEY = "test_key_123"
# Inject key for testing auth before lifespan starts
env.LITES_API_KEY = VALID_API_KEY

auth_headers = {
    "Authorization": f"Bearer {VALID_API_KEY}"
}

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Verify health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "lites-engine"}

def test_missing_authentication(client):
    """Verify API blocks unauthenticated requests."""
    response = client.post(
        "/v1/chat/completions",
        json={"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}
    )
    assert response.status_code == 401
    assert "Missing or invalid authentication scheme" in response.json()["detail"]
    
def test_invalid_authentication(client):
    """Verify API blocks invalid tokens."""
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer invalid_key"},
        json={"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}
    )
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["detail"]

def test_missing_fields(client):
    """Missing model field should fail validation."""
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={"messages": [{"role": "user", "content": "Hello"}]}
    )
    assert response.status_code == 422
    assert "model" in response.text
    
def test_invalid_fields(client):
    """Invalid types should fail validation."""
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={"model": 1234, "messages": [{"role": "user", "content": "Hello"}]} # model is not string
    )
    assert response.status_code == 422
    assert "model" in response.text

def test_empty_request(client):
    """Empty JSON body should fail."""
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={}
    )
    assert response.status_code == 422

def test_malformed_json(client):
    """Raw text instead of JSON should fail."""
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        content="this is not json"
    )
    assert response.status_code == 422

def test_oversized_request(client):
    """Extremely large prompts should fail Pydantic validation."""
    oversized_text = "A" * 500_001
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={
            "model": "gpt-4o", 
            "messages": [{"role": "user", "content": oversized_text}]
        }
    )
    assert response.status_code == 422
    assert "String should have at most 500000 characters" in response.text

@patch("app.api.server.engine.execute", new_callable=AsyncMock)
def test_valid_integration(mock_execute, client):
    """
    Valid POST request: Verify integration hits the mock provider/engine and returns valid schema.
    """
    mock_execute.return_value = "This is a mocked response from Lites."
    
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={
            "model": "gpt-4o", 
            "messages": [{"role": "user", "content": "Hello Lites!"}]
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Assert correct response schema
    assert data["model"] == "gpt-4o"
    assert data["choices"][0]["message"]["content"] == "This is a mocked response from Lites."
    assert "id" in data
    assert "usage" in data
    
    # Assert HTTP Layer headers
    assert response.headers["X-Lites-Status"] == "Success"
    assert "X-Lites-Latency-Ms" in response.headers
    
    # Assert core Lites logic was not bypassed
    mock_execute.assert_called_once()
    assert "Hello Lites!" in mock_execute.call_args[0][0]

@patch("app.api.server.engine.execute", new_callable=AsyncMock)
def test_error_responses(mock_execute, client):
    """
    Simulate ProviderError and verify error response formatting.
    """
    mock_execute.side_effect = ProviderError("OpenAI is down", status_code=502, provider="openai")
    
    response = client.post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={
            "model": "gpt-4o", 
            "messages": [{"role": "user", "content": "Hello Lites!"}]
        }
    )
    
    assert response.status_code == 502
    data = response.json()
    assert data["error"] == "provider_error"
    assert data["message"] == "OpenAI is down"
    assert data["provider"] == "openai"
