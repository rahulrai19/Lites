import pytest
from app.cache.hasher import hash_prompt

def test_hash_prompt_deterministic():
    prompt = "Explain Redis"
    model = "gpt-4o"
    assert hash_prompt(prompt, model) == hash_prompt(prompt, model)

def test_hash_differs_by_model():
    prompt = "Explain Redis"
    assert hash_prompt(prompt, "gpt-4o") != hash_prompt(prompt, "claude-3.5-sonnet")

def test_same_key_cases():
    """Verify that safe formatting differences produce consistent cache keys."""
    model = "test-model"
    base = "Explain Redis"
    
    hash_base = hash_prompt(base, model)
    hash_spaces_outer = hash_prompt(" Explain Redis ", model)
    hash_spaces_inner = hash_prompt("Explain    Redis", model)
    hash_newlines = hash_prompt("\nExplain \n\n Redis\n", model)
    
    assert hash_base == hash_spaces_outer
    assert hash_base == hash_spaces_inner
    assert hash_base == hash_newlines

def test_different_key_cases():
    """Verify meaningfully different requests remain different."""
    model = "test-model"
    hash_base = hash_prompt("Explain Redis", model)
    
    # Punctuation alters semantic meaning
    assert hash_base != hash_prompt("Explain Redis.", model)
    assert hash_base != hash_prompt("Explain Redis?", model)
    
    # Casing alters semantic meaning, especially for code and exact requirements
    assert hash_base != hash_prompt("explain redis", model)
    assert hash_base != hash_prompt("EXPLAIN REDIS", model)

def test_structured_inputs():
    """Ensure structured inputs don't suffer from destructive normalization."""
    model = "test-model"
    
    # JSON
    assert hash_prompt('{"key": "value"}', model) != hash_prompt('{"Key": "value"}', model)
    # Safe spacing normalization in JSON
    assert hash_prompt('{"key": "value"}', model) == hash_prompt('{"key":   "value"}', model)
    
    # Markdown
    assert hash_prompt('# Heading', model) != hash_prompt('## Heading', model)
    
    # Code
    assert hash_prompt('def myFunc(): pass', model) != hash_prompt('def myfunc(): pass', model)
    
    # Multi-message
    msgs1 = "system: act as a bot\nuser: hello"
    msgs2 = "system: act as a human\nuser: hello"
    assert hash_prompt(msgs1, model) != hash_prompt(msgs2, model)
