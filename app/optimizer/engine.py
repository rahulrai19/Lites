import time
from typing import List, Callable, Tuple, Optional
from app.models.optimization import OptimizationMetadata
from app.models.context import ContextProfile, CONTEXT_PROFILES
from app.optimizer.rules import (
    normalize_whitespace,
    normalize_line_endings,
    remove_duplicate_sentences,
    remove_fillers
)
from app.tokenizer.types import TokenCounter

class RuleOptimizerEngine:
    def __init__(self, token_counter: TokenCounter):
        self.token_counter = token_counter
        # Define the pipeline of deterministic rules
        self.rules: List[Callable[[str], Tuple[str, bool]]] = [
            normalize_line_endings,
            normalize_whitespace,
            remove_duplicate_sentences,
            remove_fillers
        ]

    async def optimize(self, prompt: str, model: str = "o200k_base", context: Optional[ContextProfile] = None) -> Tuple[str, OptimizationMetadata]:
        """
        Runs a prompt through the deterministic rule pipeline.
        Filters rules based on the provided ContextProfile to ensure safety.
        Measures tokens before and after, calculating the net savings.
        """
        start_time = time.perf_counter()
        
        # Resolve context mapping
        current_context = context if context is not None else ContextProfile.DEFAULT
        context_mapping = CONTEXT_PROFILES[current_context]
        
        # Count tokens before
        count_before_result = await self.token_counter.count_tokens(prompt, model)
        tokens_before = count_before_result.token_count
        
        # Apply rules sequentially
        current_prompt = prompt
        applied_operations = []
        
        for rule in self.rules:
            # Skip disabled rules for this context
            if rule.__name__ in context_mapping.disabled_rules:
                continue
            try:
                new_prompt, modified = rule(current_prompt)
                if modified:
                    current_prompt = new_prompt
                    applied_operations.append(rule.__name__)
            except Exception:
                # If a rule fails unexpectedly, we fail open (skip the rule) 
                # to preserve safety and intent.
                pass
                
        # Count tokens after
        count_after_result = await self.token_counter.count_tokens(current_prompt, model)
        tokens_after = count_after_result.token_count
        
        # Calculate savings
        tokens_saved = tokens_before - tokens_after
        
        # If somehow we increased tokens or saved 0, we can just return the original prompt
        if tokens_saved <= 0:
            current_prompt = prompt
            tokens_after = tokens_before
            tokens_saved = 0
            applied_operations = []
            
        savings_pct = (tokens_saved / tokens_before * 100) if tokens_before > 0 else 0.0
        processing_time_ms = (time.perf_counter() - start_time) * 1000.0
        
        metadata = OptimizationMetadata(
            original_prompt=prompt,
            optimized_prompt=current_prompt,
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            tokens_saved=tokens_saved,
            savings_percentage=savings_pct,
            operations_applied=applied_operations,
            optimization_applied=len(applied_operations) > 0,
            processing_time_ms=processing_time_ms
        )
        
        return current_prompt, metadata
