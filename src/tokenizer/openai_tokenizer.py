import time
import tiktoken
import re
from src.tokenizer.types import TokenCounter, TokenCountResult
from src.tokenizer.errors import InvalidModelNameError, TokenizerError

VALID_MODEL_NAME = re.compile(r"^[a-zA-Z0-9._-]+$")

class OpenAITokenizer(TokenCounter):
    @property
    def provider(self) -> str:
        return "openai"

    async def count_tokens(self, input_text: str, model: str) -> TokenCountResult:
        if not VALID_MODEL_NAME.match(model):
            raise InvalidModelNameError(model)
        
        start_time = time.perf_counter()
        
        try:
            encoding = tiktoken.encoding_for_model(model)
            is_estimate = False
        except KeyError:
            # Fallback for unrecognized models
            encoding = tiktoken.get_encoding("o200k_base")
            is_estimate = True
        
        try:
            # Using disallowed_special=() to allow any special token text to just be encoded 
            # normally rather than throwing an error, mimicking gpt-tokenizer's fallback 
            # or handling it gracefully without leaking exceptions.
            # Wait, the original ts test says: "wraps a tokenization failure (literal special-token text) in a TokenizerError"
            # If we want it to throw, we should use disallowed_special="all" (the default)
            token_count = len(encoding.encode(input_text))
        except Exception as err:
            raise TokenizerError(f'Failed to tokenize input for model "{model}": {err}', err)
            
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return TokenCountResult(
            token_count=token_count,
            model=model,
            provider=self.provider,
            source="local",
            is_estimate=is_estimate,
            latency_ms=latency_ms
        )
