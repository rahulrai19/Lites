import hashlib

def hash_prompt(prompt: str, model: str) -> str:
    """
    Generates a deterministic SHA-256 hash for a given prompt and model combination.
    This ensures that caches are segmented by the target model, as different models
    might produce different optimal responses.
    """
    # Using utf-8 encoding for standard python strings
    content = f"{model}:{prompt}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()
