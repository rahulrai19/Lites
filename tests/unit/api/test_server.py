import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.api.server import app

client = TestClient(app)

def test_chat_completions_endpoint():
    with patch("app.core.engine.LitesCoreEngine.execute") as mock_execute:
        mock_execute.return_value = "Mocked API Response"

        with TestClient(app) as client:
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "user", "content": "Hello Lites!"}
                    ]
                }
            )

        assert response.status_code == 200
        data = response.json()
        
        # Verify OpenAI schema compliance
        assert data["object"] == "chat.completion"
        assert data["model"] == "gpt-4o"
        assert len(data["choices"]) == 1
        assert data["choices"][0]["message"]["content"] == "Mocked API Response"
        assert "usage" in data
        
        # Verify Custom Headers
        assert "x-lites-status" in response.headers
        assert response.headers["x-lites-status"] == "Success"
        assert "x-lites-latency-ms" in response.headers

def test_chat_completions_invalid_context():
    with patch("app.core.engine.LitesCoreEngine.execute") as mock_execute:
        mock_execute.return_value = "Mocked API Response"

        with TestClient(app) as client:
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "user", "content": "Hello Lites!"}
                    ],
                    "x_lites_context": "invalid_profile"
                }
            )
        
        assert response.status_code == 200
        # It should fallback to DEFAULT internally and succeed
        data = response.json()
        assert data["choices"][0]["message"]["content"] == "Mocked API Response"
