from pydantic import BaseModel
import time
import asyncio

class TelemetryMetrics(BaseModel):
    total_requests: int = 0
    exact_cache_hits: int = 0
    semantic_cache_hits: int = 0
    tokens_saved_by_rules: int = 0
    tokens_saved_by_ai: int = 0
    total_optimization_overhead_ms: int = 0

class TelemetryTracker:
    def __init__(self):
        self._metrics = TelemetryMetrics()
        self._lock = asyncio.Lock()
        
    async def record_request(self):
        async with self._lock:
            self._metrics.total_requests += 1
            
    async def record_exact_cache_hit(self):
        async with self._lock:
            self._metrics.exact_cache_hits += 1
            
    async def record_semantic_cache_hit(self):
        async with self._lock:
            self._metrics.semantic_cache_hits += 1
            
    async def record_rule_savings(self, tokens: int):
        async with self._lock:
            self._metrics.tokens_saved_by_rules += max(0, tokens)
            
    async def record_ai_savings(self, tokens: int):
        async with self._lock:
            self._metrics.tokens_saved_by_ai += max(0, tokens)
            
    async def record_overhead(self, ms: int):
        async with self._lock:
            self._metrics.total_optimization_overhead_ms += ms
            
    def get_metrics(self) -> TelemetryMetrics:
        # Return a copy to avoid external mutation
        return self._metrics.model_copy()
