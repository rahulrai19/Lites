import pytest
from app.optimizer.rules import (
    normalize_whitespace,
    normalize_line_endings,
    remove_duplicate_sentences,
    remove_fillers
)
from app.optimizer.engine import RuleOptimizerEngine
from app.tokenizer.openai_tokenizer import OpenAITokenizer

def test_normalize_whitespace():
    text = "Hello    world.  How   are you?"
    expected = "Hello world. How are you?"
    new_text, modified = normalize_whitespace(text)
    assert new_text == expected
    assert modified is True

def test_normalize_whitespace_no_change():
    text = "Hello world."
    new_text, modified = normalize_whitespace(text)
    assert new_text == text
    assert modified is False

def test_normalize_line_endings():
    text = "Line 1\r\nLine 2\rLine 3"
    expected = "Line 1\nLine 2\nLine 3"
    new_text, modified = normalize_line_endings(text)
    assert new_text == expected
    assert modified is True

def test_remove_duplicate_sentences():
    text = "Explain Redis.\nExplain Redis.\nTell me more."
    expected = "Explain Redis.\nTell me more."
    new_text, modified = remove_duplicate_sentences(text)
    assert new_text == expected
    assert modified is True

def test_remove_fillers():
    text = "Can you please explain Redis to me?"
    expected = "Explain Redis to me?"
    new_text, modified = remove_fillers(text)
    assert new_text == expected
    assert modified is True

def test_remove_fillers_middle_safe():
    text = "Tell me how to say please in Spanish."
    new_text, modified = remove_fillers(text)
    assert new_text == text
    assert modified is False

@pytest.mark.asyncio
async def test_engine_optimization():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    prompt = "Can you please    explain Redis.\nCan you please    explain Redis."
    
    new_prompt, metadata = await engine.optimize(prompt, "gpt-4o")
    
    # Whitespace normalization turns spaces into one
    # Duplicate lines removes the second line
    # Fillers removes the "Can you please"
    assert new_prompt == "Explain Redis."
    assert metadata.optimization_applied is True
    assert metadata.tokens_saved > 0
    assert "remove_duplicate_sentences" in metadata.operations_applied
    assert "remove_fillers" in metadata.operations_applied
    assert "normalize_whitespace" in metadata.operations_applied
