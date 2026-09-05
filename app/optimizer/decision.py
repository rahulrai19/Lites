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
    def __init__(self, min_tokens: Optional[int] = None, max_tokens: Optional[int] = None, ai_threshold: Optional[int] = None):
        self.min_tokens = min_tokens if min_tokens is not None else env.MIN_TOKENS_FOR_OPTIMIZATION
        self.max_tokens = max_tokens if max_tokens is not None else env.MAX_TOKENS_FOR_OPTIMIZATION
        self.ai_threshold = ai_threshold if ai_threshold is not None else env.AI_OPTIMIZE_THRESHOLD

    def evaluate(self, token_count: int, expected_savings: Optional[int] = None, ai_cost: Optional[int] = None) -> DecisionResult:
        """
        Evaluates the prompt token count against configured thresholds 
        to determine the optimal optimization action.
        """
        if expected_savings is not None and expected_savings <= 0:
            return DecisionResult(
                action=OptimizationAction.SKIP,
                reason="No expected savings from optimization."
            )

        if token_count < self.min_tokens:
            return DecisionResult(
                action=OptimizationAction.SKIP,
                reason=f"Token count ({token_count}) is below the minimum threshold ({self.min_tokens}). Optimization overhead exceeds expected savings."
            )
            
        if token_count > self.max_tokens:
            return DecisionResult(
                action=OptimizationAction.CONTEXT_COMPRESS,
                reason=f"Token count ({token_count}) exceeds safe optimization threshold ({self.max_tokens}). Applying Context Compression."
            )
            
        if token_count > self.ai_threshold:
            if expected_savings is not None and ai_cost is not None and ai_cost > expected_savings:
                return DecisionResult(
                    action=OptimizationAction.SKIP,
                    reason="AI optimization costs exceed expected savings."
                )
            return DecisionResult(
                action=OptimizationAction.AI_OPTIMIZE,
                reason=f"Token count ({token_count}) exceeds the AI threshold ({self.ai_threshold}). Applying aggressive AI compression."
            )
            
        return DecisionResult(
            action=OptimizationAction.RULE_OPTIMIZE,
            reason=f"Token count ({token_count}) is within standard thresholds. Applying deterministic rules."
        )
