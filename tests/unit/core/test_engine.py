import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from app.core.engine import LitesCoreEngine
from app.core.client import MockLLMClient
from app.cache.models import CacheEntry
from app.optimizer.decision import DecisionResult, OptimizationAction

@pytest.fixture
def mock_components():
    exact_cache = AsyncMock()
    exact_cache.get.return_value = None
    
    semantic_cache = AsyncMock()
    semantic_cache.search.return_value = None
    
    embedder = AsyncMock()
    embedder.get_embedding.return_value = [0.1, 0.2, 0.3]
    
    token_counter = AsyncMock()
    count_result = MagicMock()
    count_result.token_count = 100
    token_counter.count_tokens.return_value = count_result
    
    rule_engine = AsyncMock()
    rule_engine.optimize.return_value = ("Rule Optimized Prompt", MagicMock())
    
    ai_engine = AsyncMock()
    ai_engine.optimize.return_value = ("AI Optimized Prompt", MagicMock())
    
    decision_engine = MagicMock()
    decision_engine.evaluate.return_value = DecisionResult(
        action=OptimizationAction.RULE_OPTIMIZE,
        reason="Test rule optimize"
    )
    
    llm_client = MockLLMClient(static_response="LLM Result")
    
    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=token_counter,
        rule_engine=rule_engine,
        ai_engine=ai_engine,
        decision_engine=decision_engine,
        llm_client=llm_client
    )
    
    return engine, {
        "exact_cache": exact_cache,
        "semantic_cache": semantic_cache,
        "embedder": embedder,
        "token_counter": token_counter,
        "rule_engine": rule_engine,
        "ai_engine": ai_engine,
        "decision_engine": decision_engine,
        "llm_client": llm_client
    }

@pytest.mark.asyncio
async def test_engine_exact_cache_hit_skips_pipeline(mock_components):
    engine, mocks = mock_components
    
    # Setup exact cache hit
    cached_entry = CacheEntry(
        response="Exact Hit", 
        model="test-model",
        timestamp=datetime.now()
    )
    mocks["exact_cache"].get.return_value = cached_entry
    
    response = await engine.execute("Test prompt", "test-model")
    
    assert response == "Exact Hit"
    mocks["semantic_cache"].search.assert_not_called()
    mocks["token_counter"].count_tokens.assert_not_called()
    assert mocks["llm_client"].call_count == 0

@pytest.mark.asyncio
async def test_engine_semantic_cache_hit_skips_pipeline(mock_components):
    engine, mocks = mock_components
    
    # Setup semantic cache hit
    cached_entry = CacheEntry(
        response="Semantic Hit", 
        model="test-model",
        timestamp=datetime.now()
    )
    mocks["semantic_cache"].search.return_value = cached_entry
    
    response = await engine.execute("Test prompt", "test-model")
    
    assert response == "Semantic Hit"
    mocks["exact_cache"].get.assert_called_once()
    mocks["embedder"].get_embedding.assert_called_once()
    mocks["token_counter"].count_tokens.assert_not_called()
    assert mocks["llm_client"].call_count == 0

@pytest.mark.asyncio
async def test_engine_routes_to_rule_optimization(mock_components):
    engine, mocks = mock_components
    
    response = await engine.execute("Test prompt", "test-model")
    
    assert response == "LLM Result"
    mocks["rule_engine"].optimize.assert_called_once()
    mocks["ai_engine"].optimize.assert_not_called()
    assert mocks["llm_client"].last_prompt == "Rule Optimized Prompt"
    
    # Ensure it stored to caches
    mocks["exact_cache"].set.assert_called_once()
    mocks["semantic_cache"].store.assert_called_once()

@pytest.mark.asyncio
async def test_engine_routes_to_ai_optimization(mock_components):
    engine, mocks = mock_components
    
    mocks["decision_engine"].evaluate.return_value = DecisionResult(
        action=OptimizationAction.AI_OPTIMIZE,
        reason="Test ai optimize"
    )
    
    response = await engine.execute("Test prompt", "test-model")
    
    assert response == "LLM Result"
    mocks["rule_engine"].optimize.assert_not_called()
    mocks["ai_engine"].optimize.assert_called_once()
    assert mocks["llm_client"].last_prompt == "AI Optimized Prompt"

@pytest.mark.asyncio
async def test_engine_skips_optimization(mock_components):
    engine, mocks = mock_components
    
    mocks["decision_engine"].evaluate.return_value = DecisionResult(
        action=OptimizationAction.SKIP,
        reason="Test skip"
    )
    
    response = await engine.execute("Test prompt", "test-model")
    
    assert response == "LLM Result"
    mocks["rule_engine"].optimize.assert_not_called()
    mocks["ai_engine"].optimize.assert_not_called()
    assert mocks["llm_client"].last_prompt == "Test prompt"
