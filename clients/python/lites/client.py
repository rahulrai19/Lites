import asyncio
import openai
from typing import Any, Optional, Dict, List

class LitesCompletionsCore:
    def __init__(self, engine, tokenizer, context_manager):
        self.engine = engine
        self.tokenizer = tokenizer
        self.context_manager = context_manager

    def create(self, model: str, messages: List[Dict[str, str]], lites_context: str = "default", **kwargs):
        # Sync wrapper
        return asyncio.run(self.acreate(model, messages, lites_context, **kwargs))
        
    async def acreate(self, model: str, messages: List[Dict[str, str]], lites_context: str = "default", **kwargs):
        from app.models.context import ContextProfile
        from app.api.models import Choice, ChoiceMessage, Usage, ChatCompletionResponse, ChatMessage
        import time
        
        parsed_messages = [ChatMessage(**m) for m in messages]
        full_prompt = await self.context_manager.process(
            messages=parsed_messages,
            model=model,
            max_tokens=100000,
            max_messages=100
        )
        
        try:
            context = ContextProfile(lites_context.lower())
        except ValueError:
            context = ContextProfile.DEFAULT
            
        start = time.time()
        response_text = await self.engine.execute(full_prompt, model, context)
        
        return ChatCompletionResponse(
            created=int(time.time()),
            model=model,
            choices=[
                Choice(message=ChoiceMessage(content=response_text))
            ],
            usage=Usage()
        )

class LitesChatCore:
    def __init__(self, engine, tokenizer, context_manager):
        self.completions = LitesCompletionsCore(engine, tokenizer, context_manager)

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

class Client:
    """
    Lites SDK Client.
    Supports mode='api' (default, proxy wrapping OpenAI) and mode='core' (local execution).
    """
    def __init__(
        self,
        *,
        mode: str = "api",
        api_key: Optional[str] = None,
        base_url: str | None = "http://localhost:8000/v1",
        cache_config: Optional[Dict] = None,
        **kwargs: Any,
    ) -> None:
        self.mode = mode
        if mode == "api":
            self._client = openai.Client(api_key=api_key or "dummy", base_url=base_url, **kwargs)
            self.chat = LitesChat(self._client.chat)
        elif mode == "core":
            try:
                from app.core.engine import LitesCoreEngine
                from app.core.multiplexer import HTTPMultiplexer
                from app.cache.memory import InMemoryCache
                from app.cache.semantic import InMemorySemanticCache
                from app.cache.embedder import Embedder
                from app.tokenizer.openai_tokenizer import OpenAITokenizer
                from app.optimizer.decision import DecisionEngine
                from app.optimizer.engine import RuleOptimizerEngine
                from app.optimizer.ai_engine import AIOptimizerEngine
                from app.core.context_manager import ConversationContextManager
            except ImportError:
                raise ImportError("Lites Core dependencies are not installed. Ensure the full app module is available.")
            
            # Setup Core Pipeline
            exact_cache = InMemoryCache()
            semantic_cache = InMemorySemanticCache()
            embedder = Embedder()
            tokenizer = OpenAITokenizer()
            rule_engine = RuleOptimizerEngine(tokenizer)
            ai_engine = AIOptimizerEngine(tokenizer)
            decision_engine = DecisionEngine()
            multiplexer = HTTPMultiplexer()
            context_manager = ConversationContextManager(tokenizer)
            
            self.engine = LitesCoreEngine(
                exact_cache=exact_cache,
                semantic_cache=semantic_cache,
                embedder=embedder,
                token_counter=tokenizer,
                rule_engine=rule_engine,
                ai_engine=ai_engine,
                decision_engine=decision_engine,
                llm_client=multiplexer,
                telemetry=None
            )
            self.chat = LitesChatCore(self.engine, tokenizer, context_manager)
        else:
            raise ValueError("Invalid mode. Must be 'api' or 'core'.")

class AsyncClient:
    """
    Async wrapper for Lites.
    """
    def __init__(self, mode: str = "api", api_key: Optional[str] = None, base_url: str = "http://localhost:8000/v1", **kwargs):
        self.mode = mode
        if mode == "api":
            self._client = openai.AsyncClient(api_key=api_key or "dummy", base_url=base_url, **kwargs)
            self.chat = LitesChat(self._client.chat)
        elif mode == "core":
            # Reusing the sync init which actually sets up async engines
            sync_client = Client(mode="core")
            self.engine = sync_client.engine
            
            class AsyncCompletions:
                def __init__(self, core_completions):
                    self.core = core_completions
                async def create(self, *args, **kwargs):
                    return await self.core.acreate(*args, **kwargs)
            
            class AsyncChat:
                def __init__(self, core_chat):
                    self.completions = AsyncCompletions(core_chat.completions)
                    
            self.chat = AsyncChat(sync_client.chat)
        else:
            raise ValueError("Invalid mode. Must be 'api' or 'core'.")
