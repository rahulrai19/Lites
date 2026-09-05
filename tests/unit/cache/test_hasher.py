import pytest
from app.cache.hasher import hash_prompt

def test_hash_prompt_deterministic():
    prompt = "Hello world"
    model = "gpt-4o"
    
    hash1 = hash_prompt(prompt, model)
    hash2 = hash_prompt(prompt, model)
    
    assert hash1 == hash2

def test_hash_differs_by_model():
    prompt = "Hello world"
    
    hash1 = hash_prompt(prompt, "gpt-4o")
    hash2 = hash_prompt(prompt, "claude-3.5-sonnet")
    
    assert hash1 != hash2

def test_hash_differs_by_prompt():
    model = "gpt-4o"
    
    # After normalization, these are logically different
    hash1 = hash_prompt("Hello world", model)
    hash2 = hash_prompt("Hello worlds", model)
    
    assert hash1 != hash2

def test_hash_normalization():
    model = "gpt-4o"
    
    # Capitalization differences
    hash1 = hash_prompt("Hello World", model)
    hash2 = hash_prompt("hello world", model)
    assert hash1 == hash2
    
    # Whitespace differences
    hash3 = hash_prompt("  hello    world  \n", model)
    assert hash1 == hash3
    
    # Newline differences
    hash4 = hash_prompt("hello\nworld", model)
    assert hash1 == hash4
