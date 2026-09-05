import hashlib
import re

def normalize_prompt(prompt: str) -> str:
    """
    Normalizes a prompt by converting to lowercase, stripping leading/trailing whitespace,
    and condensing multiple internal whitespaces/newlines into a single space.
    This prevents cache misses for logically identical prompts (e.g. 'Hello' vs 'hello  ').
    """
    prompt = prompt.lower().strip()
    return re.sub(r'\s+', ' ', prompt)

def hash_prompt(prompt: str, model: str) -> str:
    """
    Generates a deterministic SHA-256 hash for a given prompt and model combination.
    This ensures that caches are segmented by the target model, as different models
    might produce different optimal responses.
    """
    normalized = normalize_prompt(prompt)
    # Using utf-8 encoding for standard python strings
    content = f"{model}:{normalized}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()
