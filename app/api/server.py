import time
from fastapi import FastAPI, Response, Depends
from contextlib import asynccontextmanager

from app.api.models import ChatCompletionRequest, ChatCompletionResponse, Choice, ChoiceMessage, Usage
from app.api.auth import verify_api_key
from app.core.engine import LitesCoreEngine
from app.core.multiplexer import HTTPMultiplexer
from app.cache.memory import InMemoryCache
from app.cache.semantic import InMemorySemanticCache
from app.cache.redis_backend import RedisCache, RedisSemanticCache
from app.cache.embedder import Embedder
from app.config.env import env
from app.tokenizer.openai_tokenizer import OpenAITokenizer
from app.optimizer.decision import DecisionEngine
from app.optimizer.engine import RuleOptimizerEngine
from app.optimizer.ai_engine import AIOptimizerEngine
from app.models.context import ContextProfile
from app.telemetry.tracker import TelemetryTracker, TelemetryMetrics

# Global engine and telemetry instances
engine: LitesCoreEngine = None
telemetry: TelemetryTracker = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, telemetry
    # Initialize components
    if env.REDIS_URL:
        exact_cache = RedisCache(env.REDIS_URL)
        semantic_cache = RedisSemanticCache(env.REDIS_URL)
        print("🚀 Lites is running with persistent Redis Cache!")
    else:
        exact_cache = InMemoryCache()
        semantic_cache = InMemorySemanticCache()
        print("⚠️ Lites is running with InMemory Cache (Not recommended for production).")
        
    embedder = Embedder()
    tokenizer = OpenAITokenizer()
    rule_engine = RuleOptimizerEngine(tokenizer)
    ai_engine = AIOptimizerEngine(tokenizer)
    decision_engine = DecisionEngine()
    multiplexer = HTTPMultiplexer()
    telemetry = TelemetryTracker()
    
    engine = LitesCoreEngine(
        exact_cache=exact_cache,
        semantic_cache=semantic_cache,
        embedder=embedder,
        token_counter=tokenizer,
        rule_engine=rule_engine,
        ai_engine=ai_engine,
        decision_engine=decision_engine,
        llm_client=multiplexer,
        telemetry=telemetry
    )
    yield
    # Cleanup if necessary

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Lites Proxy API", lifespan=lifespan)

# Allow cross-origin requests from the designated frontend domain (crucial for decoupled pipelines)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[env.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Lites-Status", "X-Lites-Latency-Ms"]
)

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse, dependencies=[Depends(verify_api_key)])
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

@app.get("/v1/lites/metrics", response_model=TelemetryMetrics, dependencies=[Depends(verify_api_key)])
async def get_metrics():
    if telemetry:
        return telemetry.get_metrics()
    return TelemetryMetrics()
