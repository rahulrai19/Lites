import pytest
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.tokenizer.errors import InvalidModelNameError, TokenizerError
import json

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

# --- NEW TESTS (TEST 02 Requirements) ---

@pytest.mark.asyncio
async def test_handles_single_word(tokenizer):
    result = await tokenizer.count_tokens("Apple", "gpt-4o")
    assert result.token_count == 1
    assert result.token_count >= 0

@pytest.mark.asyncio
async def test_handles_long_prompt(tokenizer):
    text = "This is a moderately long prompt designed to test the tokenizer. " * 50
    result = await tokenizer.count_tokens(text, "gpt-4o")
    assert result.token_count > 100

@pytest.mark.asyncio
async def test_handles_repeated_text(tokenizer):
    result_single = await tokenizer.count_tokens("hello ", "gpt-4o")
    result_repeated = await tokenizer.count_tokens("hello " * 10, "gpt-4o")
    assert result_repeated.token_count > result_single.token_count
    assert result_repeated.token_count < result_single.token_count * 15 # Upper bound

@pytest.mark.asyncio
async def test_handles_multilingual_text(tokenizer):
    text = "Hello (English), Bonjour (French), 안녕하세요 (Korean), مرحبا (Arabic), नमस्ते (Hindi)."
    result = await tokenizer.count_tokens(text, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_code_snippet(tokenizer):
    code = "def fibonacci(n):\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)"
    result = await tokenizer.count_tokens(code, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_json_payload(tokenizer):
    data = {"name": "Lites", "version": "1.0", "features": ["caching", "routing"]}
    json_str = json.dumps(data)
    result = await tokenizer.count_tokens(json_str, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_markdown(tokenizer):
    md = "# Heading\n**Bold text** and *italic*.\n- Item 1\n- Item 2"
    result = await tokenizer.count_tokens(md, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_urls(tokenizer):
    url = "https://github.com/rahulrai19/Lites/tree/main/app"
    result = await tokenizer.count_tokens(url, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_special_characters(tokenizer):
    special = "!@#$%^&*()_+-=[]{}|;':,./<>?`~"
    result = await tokenizer.count_tokens(special, "gpt-4o")
    assert result.token_count > 0

@pytest.mark.asyncio
async def test_handles_extremely_large_input(tokenizer):
    text = "A" * 200000  # 200k characters
    result = await tokenizer.count_tokens(text, "gpt-4o")
    assert result.token_count > 1000

@pytest.mark.asyncio
async def test_determinism(tokenizer):
    text = "This should yield the exact same token count every single time it is run."
    result1 = await tokenizer.count_tokens(text, "gpt-4o")
    result2 = await tokenizer.count_tokens(text, "gpt-4o")
    result3 = await tokenizer.count_tokens(text, "gpt-4o")
    
    assert result1.token_count == result2.token_count == result3.token_count

@pytest.mark.asyncio
async def test_proportionality(tokenizer):
    text_short = "A quick brown fox."
    text_long = text_short * 100
    
    result_short = await tokenizer.count_tokens(text_short, "gpt-4o")
    result_long = await tokenizer.count_tokens(text_long, "gpt-4o")
    
    assert result_long.token_count > result_short.token_count

@pytest.mark.asyncio
async def test_handles_invalid_input_types(tokenizer):
    with pytest.raises(TokenizerError):
        # We expect a TokenizerError because tiktoken expects a str, passing None should throw
        await tokenizer.count_tokens(None, "gpt-4o")

@pytest.mark.asyncio
async def test_handles_special_tokens(tokenizer):
    with pytest.raises(TokenizerError):
        # Tiktoken by default throws when disallowed special tokens are present in input
        await tokenizer.count_tokens("This has a special token <|endoftext|> in it", "gpt-4o")
