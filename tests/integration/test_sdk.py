import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from clients.python.lites import Client, AsyncClient

@pytest.fixture
def mock_openai_client():
    with patch("clients.python.lites.client.openai.Client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_openai_async_client():
    with patch("clients.python.lites.client.openai.AsyncClient") as mock_client:
        yield mock_client

def test_sdk_api_mode_sync(mock_openai_client):
    """Test SDK initialization in 'api' mode (sync)."""
    client = Client(mode="api", api_key="test_key", base_url="http://mock:8000/v1")
    
    mock_openai_client.assert_called_once_with(api_key="test_key", base_url="http://mock:8000/v1")
    
    # Mock the internal original completions create
    mock_create = mock_openai_client.return_value.chat.completions.create
    mock_create.return_value = "Mocked Response"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        lites_context="test"
    )
    
    # Assert headers were injected correctly
    mock_create.assert_called_once_with(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        extra_headers={"X-Lites-Context": "test"}
    )
    assert response == "Mocked Response"

@pytest.mark.asyncio
async def test_sdk_api_mode_async(mock_openai_async_client):
    """Test SDK initialization in 'api' mode (async)."""
    client = AsyncClient(mode="api", api_key="test_key", base_url="http://mock:8000/v1")
    
    mock_openai_async_client.assert_called_once_with(api_key="test_key", base_url="http://mock:8000/v1")
    
    mock_create = AsyncMock(return_value="Mocked Async Response")
    client._client.chat.completions.create = mock_create
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello Async"}],
        lites_context="test-async"
    )
    
    mock_create.assert_called_once_with(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello Async"}],
        extra_headers={"X-Lites-Context": "test-async"}
    )
    assert response == "Mocked Async Response"

@patch("app.core.engine.LitesCoreEngine.execute", new_callable=AsyncMock)
def test_sdk_core_mode_sync(mock_execute):
    """Test SDK initialization and execution in 'core' mode (sync)."""
    client = Client(mode="core")
    
    mock_execute.return_value = "Direct Engine Response"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Core Sync Hello"}],
        lites_context="code"
    )
    
    mock_execute.assert_called_once()
    assert "Core Sync Hello" in mock_execute.call_args[0][0] # The compiled prompt
    assert response.choices[0].message.content == "Direct Engine Response"
    assert response.model == "gpt-4o"

@patch("app.core.engine.LitesCoreEngine.execute", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_sdk_core_mode_async(mock_execute):
    """Test SDK initialization and execution in 'core' mode (async)."""
    client = AsyncClient(mode="core")
    
    mock_execute.return_value = "Direct Engine Async Response"
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Core Async Hello"}],
        lites_context="code"
    )
    
    mock_execute.assert_called_once()
    assert "Core Async Hello" in mock_execute.call_args[0][0]
    assert response.choices[0].message.content == "Direct Engine Async Response"
    assert response.model == "gpt-4o"
    
def test_sdk_invalid_mode():
    """Verify invalid mode throws ValueError."""
    with pytest.raises(ValueError, match="Invalid mode"):
        Client(mode="invalid_mode")
