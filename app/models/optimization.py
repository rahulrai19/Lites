from pydantic import BaseModel, Field
from typing import List

class OptimizationMetadata(BaseModel):
    original_prompt: str
    optimized_prompt: str
    tokens_before: int
    tokens_after: int
    tokens_saved: int
    savings_percentage: float
    operations_applied: List[str] = Field(default_factory=list)
    optimization_applied: bool
    processing_time_ms: float
