from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from app.models.context import ContextProfile
from app.config.env import env

@dataclass
class RoutingDecision:
    selected_model: str
    original_model: str
    did_route: bool
    reason: str
    signals: Dict[str, Any] = field(default_factory=dict)
    estimated_cost_saved: float = 0.0

class AdaptiveRouter:
    """
    Implements Adaptive Model Routing with full explainability.
    If a user requests a highly expensive model (e.g., gpt-4o) but the task is incredibly simple
    (e.g., very few tokens and a simple context profile), Lites automatically routes the request
    to a cheaper, faster model (e.g., gemini-1.5-flash) to save costs.
    """
    def __init__(self):
        # Define expensive models that we want to optimize away from if possible
        self.expensive_models = ["gpt-4", "gpt-4-turbo", "gpt-4o", "claude-3-opus-20240229"]
        
        # Define the threshold under which a prompt is considered "simple"
        self.simple_token_threshold = 200
        
        # The fast/cheap fallback model
        self.fallback_model = "gemini-1.5-flash"
        
        # Approximate cost per 1M tokens (for estimation purposes)
        self.costs_per_1m = {
            "gpt-4o": 5.00,
            "gpt-4": 30.00,
            "gpt-4-turbo": 10.00,
            "claude-3-opus-20240229": 15.00,
            "gemini-1.5-flash": 0.075
        }

    def _estimate_cost(self, model: str, tokens: int) -> float:
        # Defaults to $5.00/1M if unknown premium model, $0.075/1M if unknown cheap model
        cost_rate = self.costs_per_1m.get(model, 5.00)
        return (tokens / 1_000_000) * cost_rate

    def route(self, prompt: str, original_model: str, token_count: int, context: ContextProfile) -> RoutingDecision:
        """
        Returns an explainable RoutingDecision object containing the target model, reason, and signals.
        """
        signals = {
            "token_count": token_count,
            "context_profile": context.name if context else "DEFAULT",
            "provider_available": bool(env.GEMINI_API_KEY)
        }
        
        # If they don't have a Gemini API Key, we can't route to Gemini
        if not env.GEMINI_API_KEY:
            return RoutingDecision(
                selected_model=original_model,
                original_model=original_model,
                did_route=False,
                reason="Routing disabled: GEMINI_API_KEY not configured for fallback model.",
                signals=signals
            )
            
        # Only route if the requested model is considered expensive
        is_expensive = any(original_model.startswith(m) for m in self.expensive_models)
        signals["is_expensive_target"] = is_expensive
        
        if is_expensive:
            # We don't route if it's CODE or LEGAL context, as those require high precision
            if context in [ContextProfile.CODE, ContextProfile.LEGAL]:
                return RoutingDecision(
                    selected_model=original_model,
                    original_model=original_model,
                    did_route=False,
                    reason=f"Routing skipped: Quality requirement too high for context '{context.name}'.",
                    signals=signals
                )
                
            # If the token count is very small, it's a simple query
            if token_count < self.simple_token_threshold:
                original_cost = self._estimate_cost(original_model, token_count)
                new_cost = self._estimate_cost(self.fallback_model, token_count)
                savings = original_cost - new_cost
                
                signals["original_estimated_cost"] = original_cost
                signals["new_estimated_cost"] = new_cost
                
                return RoutingDecision(
                    selected_model=self.fallback_model,
                    original_model=original_model,
                    did_route=True,
                    reason=f"Prompt is simple (< {self.simple_token_threshold} tokens). Routed to cheaper fallback to reduce latency and cost.",
                    signals=signals,
                    estimated_cost_saved=savings
                )
                
        return RoutingDecision(
            selected_model=original_model,
            original_model=original_model,
            did_route=False,
            reason="Prompt exceeds complexity threshold or target model is already cost-efficient.",
            signals=signals
        )
