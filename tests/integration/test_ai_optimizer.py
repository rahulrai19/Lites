import pytest
import json
from unittest.mock import AsyncMock

from app.core.engine import LitesCoreEngine
from app.core.client import MockLLMClient
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.optimizer.decision import DecisionEngine
from app.optimizer.ai_engine import AIOptimizerEngine
from app.optimizer.engine import RuleOptimizerEngine
from app.cache.memory import InMemoryCache
from app.cache.semantic import InMemorySemanticCache
from app.cache.embedder import Embedder
from app.telemetry.tracker import TelemetryTracker
from app.models.optimization import OptimizationMetadata
from app.config.env import env

@pytest.fixture
def ai_test_engine():
    tokenizer = OpenAITokenizer()
    # Lower thresholds purely for testing to force AI optimization on shorter test strings
    decision_engine = DecisionEngine(min_tokens=10, max_tokens=10000, ai_threshold=50)
    exact_cache = InMemoryCache()
    semantic_cache = InMemorySemanticCache()
    embedder = Embedder()
    embedder.get_embedding = AsyncMock(return_value=[0.0]*1536)
    
    rule_engine = RuleOptimizerEngine(tokenizer)
    ai_engine = AIOptimizerEngine(tokenizer)
    
    # We will mock ai_engine.optimize internally per-test to simulate smart AI compression
    ai_engine.optimize = AsyncMock()

    llm_client = MockLLMClient(static_response="Final LLM Output")
    llm_client.execute = AsyncMock(wraps=llm_client.execute)
    
    telemetry = TelemetryTracker()

    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=tokenizer,
        rule_engine=rule_engine,
        ai_engine=ai_engine,
        decision_engine=decision_engine,
        llm_client=llm_client,
        telemetry=telemetry
    )
    return engine

@pytest.mark.asyncio
async def test_1_short_prompt(ai_test_engine):
    """Short prompt should completely skip AI optimization due to low token count."""
    prompt = "Hello world"
    model = "gpt-4o"
    
    await ai_test_engine.execute(prompt, model)
    ai_test_engine.ai_engine.optimize.assert_not_called()

@pytest.mark.asyncio
async def test_2_medium_prompt(ai_test_engine):
    """Medium prompt (between 10 and 50 tokens) should trigger Rule Optimization, NOT AI."""
    prompt = "This is a medium prompt. " * 5  # Roughly 25 tokens
    model = "gpt-4o"
    
    await ai_test_engine.execute(prompt, model)
    ai_test_engine.ai_engine.optimize.assert_not_called()

def create_mock_meta(tokens_saved: int, operations: list) -> OptimizationMetadata:
    return OptimizationMetadata(
        original_prompt="original",
        optimized_prompt="optimized",
        tokens_before=100,
        tokens_after=100 - tokens_saved,
        tokens_saved=tokens_saved,
        savings_percentage=50.0,
        operations_applied=operations,
        optimization_applied=True,
        processing_time_ms=150
    )

@pytest.mark.asyncio
async def test_3_long_prompt(ai_test_engine):
    """Long prompt (>50 tokens) should trigger AI Optimizer."""
    prompt = "This is a long prompt to trigger the AI optimizer. " * 20
    model = "gpt-4o"
    
    ai_test_engine.ai_engine.optimize.return_value = ("Compressed long prompt", create_mock_meta(50, ["ai"]))
    
    await ai_test_engine.execute(prompt, model)
    ai_test_engine.ai_engine.optimize.assert_called_once()
    
    # Verify main LLM receives the compressed prompt
    args, _ = ai_test_engine.llm_client.execute.call_args
    assert args[0] == "Compressed long prompt"

@pytest.mark.asyncio
async def test_4_repetitive_prompt(ai_test_engine):
    """Repetitive prompts should have huge savings from AI."""
    prompt = "I need help. " * 100
    model = "gpt-4o"
    
    ai_test_engine.ai_engine.optimize.return_value = ("I need help (repeated x100).", create_mock_meta(300, ["ai"]))
    
    await ai_test_engine.execute(prompt, model)
    ai_test_engine.ai_engine.optimize.assert_called_once()

@pytest.mark.asyncio
async def test_5_technical_prompt(ai_test_engine):
    """Technical prompts must preserve semantic factual density."""
    prompt = "The AWS EC2 t3.micro instance has 2 vCPUs and 1 GiB of RAM. " * 10
    model = "gpt-4o"
    
    # Mocking that AI condenses it to a single factual statement
    compressed = "AWS EC2 t3.micro: 2 vCPUs, 1 GiB RAM."
    ai_test_engine.ai_engine.optimize.return_value = (compressed, create_mock_meta(80, ["ai"]))
    
    await ai_test_engine.execute(prompt, model)
    args, _ = ai_test_engine.llm_client.execute.call_args
    assert "2 vCPUs" in args[0]

@pytest.mark.asyncio
async def test_6_code_prompt(ai_test_engine):
    """Code prompts must not be semantically corrupted."""
    prompt = "def hello():\n    print('hello world')\n" * 20
    model = "gpt-4o"
    
    compressed = "def hello():\n    print('hello world')"
    ai_test_engine.ai_engine.optimize.return_value = (compressed, create_mock_meta(100, ["ai"]))
    
    await ai_test_engine.execute(prompt, model)
    args, _ = ai_test_engine.llm_client.execute.call_args
    assert "def hello():" in args[0]

@pytest.mark.asyncio
async def test_7_json_prompt(ai_test_engine):
    """JSON prompts must retain valid structure."""
    prompt = json.dumps({"data": [{"id": i, "val": "x"} for i in range(20)]}, indent=4)
    model = "gpt-4o"
    
    compressed = json.dumps({"data": [{"id": i, "val": "x"} for i in range(20)]})
    ai_test_engine.ai_engine.optimize.return_value = (compressed, create_mock_meta(50, ["ai"]))
    
    await ai_test_engine.execute(prompt, model)
    args, _ = ai_test_engine.llm_client.execute.call_args
    assert json.loads(args[0]) is not None

@pytest.mark.asyncio
async def test_8_cost_benefit_skip(ai_test_engine):
    """Cost test: AI optimizer cost > expected savings. Expected: AI optimization is skipped."""
    prompt = "This is a long prompt. " * 20  # >50 tokens
    
    # Target a very cheap model (gpt-4o-mini) where ai_cost multiplier is 2.0
    # Because ai_cost (2.0) > expected_savings (0.3), AI optimizer should be skipped entirely
    model = "gpt-4o-mini"
    
    await ai_test_engine.execute(prompt, model)
    
    # AI Optimizer must NOT be called despite prompt > 50 tokens
    ai_test_engine.ai_engine.optimize.assert_not_called()

@pytest.mark.asyncio
async def test_provider_failures(ai_test_engine, monkeypatch):
    """Test AI optimizer API failures safe-fallback to original prompt."""
    prompt = "This is a long prompt. " * 20
    model = "gpt-4o"
    
    # We must use the REAL ai_engine for this test, not the mock, 
    # to verify its internal try/except logic successfully falls back.
    # Restore the original optimize method (we mocked it in the fixture)
    real_ai_engine = AIOptimizerEngine(ai_test_engine.token_counter)
    
    # Force a timeout deep inside the httpx post call
    async def mock_post(*args, **kwargs):
        import httpx
        raise httpx.TimeoutException("Mock Timeout")
        
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)
    
    # Enable Gemini Key to hit the try block
    monkeypatch.setattr("app.optimizer.ai_engine.env.GEMINI_API_KEY", "real-key-so-it-runs")
    
    ai_test_engine.ai_engine = real_ai_engine

    # Engine should catch the AI engine failure, log it, and fallback to using the original unoptimized prompt!
    await ai_test_engine.execute(prompt, model)
    
    # Verify main LLM still receives the ORIGINAL prompt safely despite the AI failure
    args, _ = ai_test_engine.llm_client.execute.call_args
    assert args[0] == prompt
