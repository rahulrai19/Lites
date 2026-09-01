from typing import Literal
from pydantic import BaseModel

TokenizerSource = Literal['local', 'api']

class TokenCountResult(BaseModel):
    token_count: int
    model: str
    provider: str
    source: TokenizerSource
    is_estimate: bool
    latency_ms: float

class TokenCounter:
    @property
    def provider(self) -> str:
        raise NotImplementedError

    async def count_tokens(self, input_text: str, model: str) -> TokenCountResult:
        raise NotImplementedError
