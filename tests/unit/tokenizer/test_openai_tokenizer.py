import pytest
from src.tokenizer.openai_tokenizer import OpenAITokenizer
from src.tokenizer.errors import InvalidModelNameError, TokenizerError

@pytest.fixture
def tokenizer():
    return OpenAITokenizer()

def test_reports_provider(tokenizer):
    assert tokenizer.provider == "openai"

@pytest.mark.asyncio
async def test_counts_tokens_for_recognized_model(tokenizer):
    result = await tokenizer.count_tokens("Hello, world!", "gpt-4o")
    
    assert result.token_count > 0
    assert result.model == "gpt-4o"
    assert result.provider == "openai"
    assert result.source == "local"
    assert result.is_estimate is False
    assert result.latency_ms >= 0

@pytest.mark.asyncio
async def test_produces_same_count_for_known_text(tokenizer):
    result = await tokenizer.count_tokens("Hello, world!", "gpt-4o")
    assert result.token_count == 4

@pytest.mark.asyncio
async def test_falls_back_to_default_encoding(tokenizer):
    result = await tokenizer.count_tokens("Hello, world!", "not-a-real-model-xyz")
    
    assert result.token_count > 0
    assert result.model == "not-a-real-model-xyz"
    assert result.is_estimate is True

@pytest.mark.asyncio
async def test_rejects_invalid_model_names(tokenizer):
    with pytest.raises(InvalidModelNameError):
        await tokenizer.count_tokens("hi", "../../etc/passwd")

@pytest.mark.asyncio
async def test_returns_zero_for_empty_string(tokenizer):
    result = await tokenizer.count_tokens("", "gpt-4o")
    assert result.token_count == 0

@pytest.mark.asyncio
async def test_handles_unicode(tokenizer):
    result = await tokenizer.count_tokens("🚀—hello世界", "gpt-4o")
    assert result.token_count > 0
