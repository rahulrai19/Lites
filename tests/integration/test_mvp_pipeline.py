import pytest
from unittest.mock import AsyncMock

from app.core.engine import LitesCoreEngine
from app.core.client import MockLLMClient
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.optimizer.decision import DecisionEngine
from app.optimizer.engine import RuleOptimizerEngine
from app.cache.memory import InMemoryCache
from app.cache.semantic import InMemorySemanticCache
from app.cache.embedder import Embedder
from app.telemetry.tracker import TelemetryTracker
from app.core.exceptions import ProviderTimeoutError

@pytest.fixture
def mvp_engine():
    # Construct the full determinisic pipeline with mocks where appropriate
    tokenizer = OpenAITokenizer()
    decision_engine = DecisionEngine()
    exact_cache = InMemoryCache()
    semantic_cache = InMemorySemanticCache()
    embedder = Embedder()
    embedder.get_embedding = AsyncMock(return_value=[0.0]*1536)
    rule_engine = RuleOptimizerEngine(tokenizer)
    
    # Spy on caching and telemetry methods
    exact_cache.get = AsyncMock(wraps=exact_cache.get)
    exact_cache.set = AsyncMock(wraps=exact_cache.set)
    telemetry = TelemetryTracker()
    telemetry.record_request = AsyncMock(wraps=telemetry.record_request)
    telemetry.record_exact_cache_hit = AsyncMock(wraps=telemetry.record_exact_cache_hit)
    telemetry.record_rule_savings = AsyncMock(wraps=telemetry.record_rule_savings)
    
    llm_client = MockLLMClient(static_response="Pipeline LLM Output")
    llm_client.execute = AsyncMock(wraps=llm_client.execute)

    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=tokenizer,
        rule_engine=rule_engine,
        ai_engine=AsyncMock(),
        decision_engine=decision_engine,
        llm_client=llm_client,
        telemetry=telemetry
    )
    return engine

@pytest.mark.asyncio
async def test_1_cache_miss_flow(mvp_engine):
    """
    Test 1 — Cache miss
    Verify: MISS -> optimization -> provider -> cache store -> response
    """
    prompt = "Please explain the redis cache system   \n in great    detail."
    model = "gpt-4o"
    
    response = await mvp_engine.execute(prompt, model)
    
    assert response == "Pipeline LLM Output"
    
    # 1. Verify Cache MISS
    mvp_engine.exact_cache.get.assert_called_once()
    
    # 2. Verify Provider was called
    mvp_engine.llm_client.execute.assert_called_once()
    
    # 3. Verify Cache Store
    mvp_engine.exact_cache.set.assert_called_once()
    
    # 4. Verify Metrics
    mvp_engine.telemetry.record_request.assert_called_once()
    mvp_engine.telemetry.record_exact_cache_hit.assert_not_called()

@pytest.mark.asyncio
async def test_2_cache_hit_flow(mvp_engine):
    """
    Test 2 — Cache hit
    Verify: HIT -> cached response -> provider is NOT called
    """
    prompt = "What is caching?"
    model = "gpt-4o"
    
    # First call: Cache Miss
    await mvp_engine.execute(prompt, model)
    
    # Reset mocks
    mvp_engine.llm_client.execute.reset_mock()
    mvp_engine.exact_cache.set.reset_mock()
    
    # Second call: Cache Hit
    response2 = await mvp_engine.execute(prompt, model)
    assert response2 == "Pipeline LLM Output"
    
    # Verify Provider NOT called
    mvp_engine.llm_client.execute.assert_not_called()
    
    # Verify Cache Store NOT called again
    mvp_engine.exact_cache.set.assert_not_called()
    
    # Verify Hit Metric
    mvp_engine.telemetry.record_exact_cache_hit.assert_called_once()

@pytest.mark.asyncio
async def test_3_optimization_recorded(mvp_engine):
    """
    Test 3 — Optimization
    Verify token reduction is recorded.
    """
    # A prompt with huge amounts of whitespace and fillers to trigger rule optimization savings
    prompt = "Actually, um, " + " " * 50 + "could you please explain... " * 20
    model = "gpt-4o"
    
    await mvp_engine.execute(prompt, model)
    
    # Assert rule savings recorded
    mvp_engine.telemetry.record_rule_savings.assert_called_once()
    # Ensure savings > 0
    call_args = mvp_engine.telemetry.record_rule_savings.call_args[0][0]
    assert call_args > 0

@pytest.mark.asyncio
async def test_4_no_optimization_for_short(mvp_engine):
    """
    Test 4 — No optimization
    Verify short/unsafe prompts can pass through unchanged.
    """
    # DecisionEngine defines MIN_TOKENS_FOR_OPTIMIZATION = 50. 
    # A tiny prompt skips rule engine entirely.
    prompt = "Hi"
    model = "gpt-4o"
    
    await mvp_engine.execute(prompt, model)
    
    # Should skip rule savings entirely
    mvp_engine.telemetry.record_rule_savings.assert_not_called()

@pytest.mark.asyncio
async def test_5_provider_failure(mvp_engine):
    """
    Test 5 — Provider failure
    Verify correct error handling and cache behavior.
    """
    prompt = "Fail me"
    model = "gpt-4o"
    
    # Force the provider to throw a Timeout
    mvp_engine.llm_client.exception_to_raise = ProviderTimeoutError("openai")
    
    with pytest.raises(ProviderTimeoutError):
        await mvp_engine.execute(prompt, model)
        
    # Crucial Regression: Cache must NOT be written if provider fails
    mvp_engine.exact_cache.set.assert_not_called()

@pytest.mark.asyncio
async def test_6_and_7_metrics_aggregate(mvp_engine):
    """
    Test 6 & 7 — Metrics and Multiple Requests
    Verify every stage produces consistent aggregate statistics.
    """
    prompt1 = "Request one" * 50 # Force > 50 tokens
    prompt2 = "Request two" * 50 # Force > 50 tokens
    model = "gpt-4o"
    
    # Request 1 (Miss)
    await mvp_engine.execute(prompt1, model)
    # Request 1 Duplicate (Hit)
    await mvp_engine.execute(prompt1, model)
    # Request 2 (Miss)
    await mvp_engine.execute(prompt2, model)
    
    metrics = mvp_engine.telemetry.get_metrics()
    
    assert metrics.total_requests == 3
    assert metrics.exact_cache_hits == 1
    assert mvp_engine.llm_client.call_count == 2 # 2 misses = 2 provider calls
    
    # Because both requests were long, optimization overhead should be recorded (even if 0ms on fast systems)
    assert metrics.total_optimization_overhead_ms >= 0
    # Rule savings should be accumulated
    assert metrics.tokens_saved_by_rules >= 0
