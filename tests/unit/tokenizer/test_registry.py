import pytest
from src.tokenizer.registry import TokenizerRegistry
from src.tokenizer.errors import UnsupportedProviderError
from src.tokenizer.types import TokenCounter, TokenCountResult

class FakeTokenCounter(TokenCounter):
    def __init__(self, provider: str):
        self._provider = provider

    @property
    def provider(self) -> str:
        return self._provider

    async def count_tokens(self, input_text: str, model: str) -> TokenCountResult:
        return TokenCountResult(
            token_count=len(input_text),
            model=model,
            provider=self.provider,
            source="local",
            is_estimate=False,
            latency_ms=0.0
        )

def test_registry_starts_empty():
    registry = TokenizerRegistry()
    assert registry.list_providers() == []

def test_registers_and_retrieves_counter():
    registry = TokenizerRegistry()
    fake = FakeTokenCounter("openai")
    registry.register(fake)

    assert registry.has("openai") is True
    assert registry.get("openai") == fake
    assert registry.list_providers() == ["openai"]

def test_supports_multiple_providers():
    registry = TokenizerRegistry()
    registry.register(FakeTokenCounter("openai"))
    registry.register(FakeTokenCounter("fake-provider"))

    providers = registry.list_providers()
    providers.sort()
    assert providers == ["fake-provider", "openai"]

def test_throws_for_unregistered_provider():
    registry = TokenizerRegistry()
    registry.register(FakeTokenCounter("openai"))

    with pytest.raises(UnsupportedProviderError, match="openai"):
        registry.get("anthropic")

def test_separate_registries_do_not_share_state():
    a = TokenizerRegistry()
    b = TokenizerRegistry()

    a.register(FakeTokenCounter("openai"))

    assert a.has("openai") is True
    assert b.has("openai") is False
