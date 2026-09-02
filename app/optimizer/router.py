from typing import Tuple
from app.models.context import ContextProfile
from app.config.env import env

class AdaptiveRouter:
    """
    Implements Adaptive Model Routing (Optimization #5).
    If a user requests a highly expensive model (e.g., gpt-4) but the task is incredibly simple
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

    def route(self, prompt: str, original_model: str, token_count: int, context: ContextProfile) -> Tuple[str, bool]:
        """
        Returns a tuple: (Target Model, Did Route?)
        """
        # If they don't have a Gemini API Key, we can't route to Gemini
        if not env.GEMINI_API_KEY:
            return original_model, False
            
        # Only route if the requested model is considered expensive
        is_expensive = any(original_model.startswith(m) for m in self.expensive_models)
        
        if is_expensive:
            # We don't route if it's CODE or LEGAL context, as those require high precision
            if context in [ContextProfile.CODE, ContextProfile.LEGAL]:
                return original_model, False
                
            # If the token count is very small, it's a simple query
            if token_count < self.simple_token_threshold:
                return self.fallback_model, True
                
        return original_model, False
