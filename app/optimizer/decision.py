from enum import Enum
from dataclasses import dataclass
from typing import Optional

from app.config.env import env

class OptimizationAction(str, Enum):
    SKIP = "skip"
    RULE_OPTIMIZE = "rule_optimize"
    CONTEXT_COMPRESS = "context_compress"
    AI_OPTIMIZE = "ai_optimize"

@dataclass
class DecisionResult:
    action: OptimizationAction
    reason: str

class DecisionEngine:
    def __init__(self, min_tokens: Optional[int] = None, max_tokens: Optional[int] = None):
        self.min_tokens = min_tokens if min_tokens is not None else env.MIN_TOKENS_FOR_OPTIMIZATION
        self.max_tokens = max_tokens if max_tokens is not None else env.MAX_TOKENS_FOR_OPTIMIZATION

    def evaluate(self, token_count: int) -> DecisionResult:
        """
        Evaluates the prompt token count against configured thresholds 
        to determine the optimal optimization action.
        """
        if token_count < self.min_tokens:
            return DecisionResult(
                action=OptimizationAction.SKIP,
                reason=f"Token count ({token_count}) is below the minimum threshold ({self.min_tokens}). Optimization overhead exceeds expected savings."
            )
            
        if token_count > self.max_tokens:
            return DecisionResult(
                action=OptimizationAction.SKIP,
                reason=f"Token count ({token_count}) exceeds the maximum threshold ({self.max_tokens}) for safe optimization."
            )
            
        # Default to RULE_OPTIMIZE for now, as AI/Context optimization are future phases
        return DecisionResult(
            action=OptimizationAction.RULE_OPTIMIZE,
            reason=f"Token count ({token_count}) is within thresholds. Applying deterministic rules."
        )
