import time
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager

from app.api.models import ChatCompletionRequest, ChatCompletionResponse, Choice, ChoiceMessage, Usage
from app.core.engine import LitesCoreEngine
from app.core.multiplexer import HTTPMultiplexer
from app.cache.memory import InMemoryCache
from app.cache.semantic import InMemorySemanticCache
from app.cache.embedder import Embedder
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.optimizer.decision import DecisionEngine
from app.optimizer.engine import RuleOptimizerEngine
from app.optimizer.ai_engine import AIOptimizerEngine
from app.models.context import ContextProfile

# Global engine instance
engine: LitesCoreEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    # Initialize components
    exact_cache = InMemoryCache()
    semantic_cache = InMemorySemanticCache()
    embedder = Embedder()
    tokenizer = OpenAITokenizer()
    rule_engine = RuleOptimizerEngine(tokenizer)
    ai_engine = AIOptimizerEngine(tokenizer)
    decision_engine = DecisionEngine()
    multiplexer = HTTPMultiplexer()
    
    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=tokenizer,
        rule_engine=rule_engine,
        ai_engine=ai_engine,
        decision_engine=decision_engine,
        llm_client=multiplexer
    )
    yield
    # Cleanup if necessary

app = FastAPI(title="Lites Proxy API", lifespan=lifespan)

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest, response: Response):
    # Combine messages into a single string for optimization
    # In a real production proxy, we would preserve message boundaries.
    full_prompt = "\n".join([msg.content for msg in request.messages])
    
    # Parse context profile
    try:
        context = ContextProfile(request.x_lites_context.lower())
    except ValueError:
        context = ContextProfile.DEFAULT
        
    # Execute through the Lites Core Engine
    # Note: Engine currently returns only the string response. 
    # To return metadata headers, we'd ideally return the metadata from execute().
    # For now, we will execute and inject a basic X-Lites-Status header.
    start_time = time.time()
    
    response_text = await engine.execute(full_prompt, request.model, context)
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    
    # Inject Lites Headers
    response.headers["X-Lites-Status"] = "Success"
    response.headers["X-Lites-Latency-Ms"] = str(elapsed_ms)
    
    return ChatCompletionResponse(
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                message=ChoiceMessage(content=response_text)
            )
        ],
        usage=Usage()
    )
