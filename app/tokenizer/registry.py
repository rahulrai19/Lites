from typing import Dict, List
from app.tokenizer.types import TokenCounter
from app.tokenizer.errors import UnsupportedProviderError

class TokenizerRegistry:
    def __init__(self):
        self._counters: Dict[str, TokenCounter] = {}

    def register(self, counter: TokenCounter) -> None:
        self._counters[counter.provider] = counter

    def get(self, provider: str) -> TokenCounter:
        counter = self._counters.get(provider)
        if not counter:
            raise UnsupportedProviderError(provider, self.list_providers())
        return counter

    def has(self, provider: str) -> bool:
        return provider in self._counters

    def list_providers(self) -> List[str]:
        return list(self._counters.keys())
