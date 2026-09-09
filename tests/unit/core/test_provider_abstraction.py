import pytest
from unittest.mock import AsyncMock

from app.core.engine import LitesCoreEngine
from app.core.client import MockLLMClient
from app.core.exceptions import (
    ProviderError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    ProviderMalformedResponseError,
    ProviderEmptyResponseError
)
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.optimizer.decision import DecisionEngine
from app.cache.memory import InMemoryCache
from app.cache.semantic import InMemorySemanticCache
from app.cache.embedder import Embedder
from app.cache.embedder import Embedder

@pytest.fixture
def base_engine():
    tokenizer = OpenAITokenizer()
    decision_engine = DecisionEngine()
    exact_cache = InMemoryCache()
    semantic_cache = InMemorySemanticCache()
    embedder = Embedder()
    
    # We will override llm_client per test
    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=tokenizer,
        rule_engine=AsyncMock(), # not needed for these tests
        ai_engine=AsyncMock(),   # not needed for these tests
        decision_engine=decision_engine,
        llm_client=MockLLMClient(),
        telemetry=None
    )
    
    # Spy on the cache to verify regression constraint
    engine.exact_cache.set = AsyncMock(wraps=engine.exact_cache.set)
    return engine

@pytest.mark.asyncio
async def test_successful_response(base_engine):
    base_engine.llm_client = MockLLMClient(static_response="Success!")
    
    response = await base_engine.execute("Test prompt", "gpt-4o")
    
    assert response == "Success!"
    # Ensure cache set WAS called for success
    base_engine.exact_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_provider_timeout_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderTimeoutError("openai"))
    
    with pytest.raises(ProviderTimeoutError):
        await base_engine.execute("Test prompt", "gpt-4o")
        
    # Regression: ensure cache was NOT corrupted
    base_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_provider_auth_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderAuthenticationError("gemini"))
    
    with pytest.raises(ProviderAuthenticationError):
        await base_engine.execute("Test prompt", "gemini-1.5")
        
    base_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_provider_rate_limit_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderRateLimitError("openai"))
    
    with pytest.raises(ProviderRateLimitError):
        await base_engine.execute("Test prompt", "gpt-4o")
        
    base_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_provider_general_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderError("Bad Gateway", "openai", 502))
    
    with pytest.raises(ProviderError):
        await base_engine.execute("Test prompt", "gpt-4o")
        
    base_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_provider_malformed_response_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderMalformedResponseError("gemini", "KeyError: 'candidates'"))
    
    with pytest.raises(ProviderMalformedResponseError):
        await base_engine.execute("Test prompt", "gemini-1.5")
        
    base_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_provider_empty_response_error(base_engine):
    base_engine.llm_client = MockLLMClient(exception_to_raise=ProviderEmptyResponseError("openai"))
    
    with pytest.raises(ProviderEmptyResponseError):
        await base_engine.execute("Test prompt", "gpt-4o")
        
    base_engine.exact_cache.set.assert_not_called()
