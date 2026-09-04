import pytest
from unittest.mock import AsyncMock
from app.optimizer.engine import RuleOptimizerEngine
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.models.context import ContextProfile

@pytest.fixture
def tokenizer():
    return OpenAITokenizer()

@pytest.fixture
def engine(tokenizer):
    return RuleOptimizerEngine(tokenizer)

@pytest.mark.asyncio
async def test_metrics_no_optimization(engine):
    prompt = "This is a perfect prompt."
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert metadata.tokens_before == metadata.tokens_after
    assert metadata.tokens_saved == 0
    assert metadata.savings_percentage == 0.0
    assert metadata.optimization_applied is False
    assert len(metadata.operations_applied) == 0
    assert metadata.processing_time_ms > 0

@pytest.mark.asyncio
async def test_metrics_small_optimization(engine):
    # One extra space should trigger normalize_whitespace but save 0 tokens likely
    # Let's use a filler word so we definitively save a token
    prompt = "Please run this command."
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert metadata.tokens_saved > 0
    assert metadata.tokens_before > metadata.tokens_after
    assert metadata.savings_percentage > 0.0
    assert metadata.optimization_applied is True
    assert len(metadata.operations_applied) > 0
    assert metadata.processing_time_ms > 0

@pytest.mark.asyncio
async def test_metrics_large_optimization(engine):
    # A massive paragraph of fillers and duplicated sentences
    base_sentence = "Please kind sir, could you possibly help me with this task.\n"
    prompt = base_sentence * 20
    
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    # It should collapse all duplicated sentences and strip fillers
    assert metadata.tokens_saved > 0
    assert metadata.savings_percentage > 50.0  # Should be massively reduced
    assert metadata.optimization_applied is True

@pytest.mark.asyncio
async def test_metrics_multiple_optimizations(engine):
    # Should trigger normalize_whitespace, remove_fillers, remove_duplicate_sentences
    prompt = "Please    do    this. Please    do    this."
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert metadata.tokens_saved > 0
    assert len(metadata.operations_applied) >= 2
    assert metadata.optimization_applied is True

@pytest.mark.asyncio
async def test_metrics_optimization_increases_tokens(engine):
    # We will mock the tokenizer to pretend the optimization INCREASED tokens
    # to test the failsafe.
    mock_tokenizer = AsyncMock()
    
    # First call (before optimization): 10 tokens
    # Second call (after optimization): 15 tokens
    mock_count_before = AsyncMock()
    mock_count_before.token_count = 10
    
    mock_count_after = AsyncMock()
    mock_count_after.token_count = 15
    
    mock_tokenizer.count_tokens.side_effect = [mock_count_before, mock_count_after]
    
    mock_engine = RuleOptimizerEngine(mock_tokenizer)
    
    prompt = "Please do this."
    _, metadata = await mock_engine.optimize(prompt, "gpt-4o")
    
    # Since tokens increased, engine must revert
    assert metadata.tokens_saved == 0
    assert metadata.tokens_after == 10  # Reverted back to original
    assert metadata.savings_percentage == 0.0
    assert metadata.optimization_applied is False
    assert len(metadata.operations_applied) == 0

@pytest.mark.asyncio
async def test_metrics_empty_prompt(engine):
    prompt = ""
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert metadata.tokens_before == 0
    assert metadata.tokens_after == 0
    assert metadata.tokens_saved == 0
    assert metadata.savings_percentage == 0.0
    assert metadata.optimization_applied is False

@pytest.mark.asyncio
async def test_metrics_regression_no_negative_savings(engine):
    # Edge case: tokenizers might evaluate a trailing space weirdly.
    prompt = "Test \n \n"
    _, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert metadata.tokens_saved >= 0
    assert metadata.savings_percentage >= 0.0
