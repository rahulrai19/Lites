import openai
from typing import Any, Mapping

class LitesCompletions:
    def __init__(self, original_completions):
        self._original = original_completions

    def create(self, *args, lites_context: str = None, **kwargs):
        if lites_context:
            extra_headers = kwargs.get("extra_headers", {})
            extra_headers["X-Lites-Context"] = lites_context
            kwargs["extra_headers"] = extra_headers
        return self._original.create(*args, **kwargs)

class LitesChat:
    def __init__(self, original_chat):
        self.completions = LitesCompletions(original_chat.completions)

class Client(openai.Client):
    """
    A thin wrapper around openai.Client that automatically points to 
    the local Lites proxy and injects X-Lites custom headers.
    """
    def __init__(
        self,
        *,
        base_url: str | None = "http://localhost:8000/v1",
        **kwargs: Any,
    ) -> None:
        super().__init__(base_url=base_url, **kwargs)
        
        # Wrap the chat.completions endpoint
        self.chat = LitesChat(self.chat)
