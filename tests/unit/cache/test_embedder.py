import pytest
from unittest.mock import patch, MagicMock
from app.cache.embedder import Embedder
from app.config.env import env

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setattr(env, "OPENAI_API_KEY", "test-key-123")

@pytest.mark.asyncio
async def test_embedder_returns_vector(mock_env):
    embedder = Embedder()
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [{"embedding": [0.1, 0.2, 0.3]}]
    }
    
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_instance = mock_client_class.return_value.__aenter__.return_value
        mock_client_instance.post.return_value = mock_response
        
        result = await embedder.get_embedding("Hello world")
        
        assert result == [0.1, 0.2, 0.3]

@pytest.mark.asyncio
async def test_embedder_skips_without_api_key(monkeypatch):
    monkeypatch.setattr(env, "OPENAI_API_KEY", "")
    
    embedder = Embedder()
    result = await embedder.get_embedding("Hello world")
    
    assert result is None

@pytest.mark.asyncio
async def test_embedder_handles_api_failure(mock_env):
    embedder = Embedder()
    
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client_instance = mock_client_class.return_value.__aenter__.return_value
        mock_client_instance.post.side_effect = Exception("API Down")
        
        result = await embedder.get_embedding("Hello world")
        
        assert result is None
