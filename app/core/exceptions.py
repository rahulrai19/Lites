class LitesError(Exception):
    """Base exception for all Lites engine errors."""
    pass

class ProviderError(LitesError):
    """Base exception for errors originating from downstream LLM providers."""
    def __init__(self, message: str, provider: str, status_code: int = 500):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code
        self.message = message

class ProviderTimeoutError(ProviderError):
    """Raised when a downstream provider times out."""
    def __init__(self, provider: str):
        super().__init__(f"Timeout while contacting {provider}", provider, 504)

class ProviderAuthenticationError(ProviderError):
    """Raised when the Lites engine fails to authenticate with a downstream provider."""
    def __init__(self, provider: str):
        super().__init__(f"Authentication failed for {provider}", provider, 502)

class ProviderRateLimitError(ProviderError):
    """Raised when a downstream provider rate limits the Lites engine."""
    def __init__(self, provider: str):
        super().__init__(f"Rate limit exceeded for {provider}", provider, 429)

class ProviderMalformedResponseError(ProviderError):
    """Raised when a downstream provider returns a response that cannot be parsed."""
    def __init__(self, provider: str, details: str):
        super().__init__(f"Malformed response from {provider}: {details}", provider, 502)

class ProviderEmptyResponseError(ProviderError):
    """Raised when a downstream provider returns an empty response."""
    def __init__(self, provider: str):
        super().__init__(f"Empty response received from {provider}", provider, 502)
