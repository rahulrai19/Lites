from typing import Protocol, Any, Dict
from datetime import datetime

class LLMClient(Protocol):
    """Protocol defining how the Lites proxy talks to downstream providers (OpenAI, Anthropic, etc)."""
    async def execute(self, prompt: str, model: str) -> str:
        ...

class MockLLMClient:
    """A mock client used for unit testing the Core Engine orchestration."""
    def __init__(self, static_response: str = "Mocked LLM Response"):
        self.static_response = static_response
        self.call_count = 0
        self.last_prompt = None
        self.last_model = None

    async def execute(self, prompt: str, model: str) -> str:
        self.call_count += 1
        self.last_prompt = prompt
        self.last_model = model
        return self.static_response
