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
    
    hash1 = hash_prompt("Hello world", model)
    hash2 = hash_prompt("Hello world!", model)
    
    assert hash1 != hash2
