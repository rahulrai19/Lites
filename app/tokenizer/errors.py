from typing import Optional, List

class TokenizerError(Exception):
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause

class UnsupportedProviderError(TokenizerError):
    def __init__(self, provider: str, known_providers: List[str]):
        known = ", ".join(known_providers) if known_providers else "(none registered)"
        super().__init__(f'No tokenizer registered for provider "{provider}". Known providers: {known}')

class InvalidModelNameError(TokenizerError):
    def __init__(self, model: str):
        super().__init__(f'"{model}" is not a valid model identifier.')
