import json
import os
import time
import asyncio
from typing import Optional
from pydantic import BaseModel

class TelemetryMetrics(BaseModel):
    total_requests: int = 0
    exact_cache_hits: int = 0
    exact_cache_misses: int = 0
    semantic_cache_hits: int = 0
    semantic_cache_misses: int = 0
    total_tokens_processed: int = 0
    tokens_saved_by_rules: int = 0
    tokens_saved_by_ai: int = 0
    total_optimization_overhead_ms: int = 0
    provider_latency_ms: int = 0
    total_latency_ms: int = 0
    total_estimated_cost_saved: float = 0.0
    total_routing_redirects: int = 0

class TelemetryTracker:
    def __init__(self, mongo_client=None, redis_client=None, file_path="data/metrics.json"):
        self._metrics = TelemetryMetrics()
        self._lock = asyncio.Lock()
        self._mongo_client = mongo_client
        self._redis_client = redis_client
        self._file_path = file_path
        self._collection = None
        self._sync_task = None
        self._dirty = False
        
        if self._mongo_client is not None:
            self._collection = self._mongo_client["lites"]["metrics"]

    async def initialize(self):
        """Loads historical metrics from Redis, MongoDB, or local file, and starts the sync loop."""
        loaded = False
        
        # 1. Try Redis first (fast and persistent)
        if self._redis_client is not None:
            try:
                cached_data = await self._redis_client.get("lites:global_metrics")
                if cached_data:
                    parsed = json.loads(cached_data)
                    self._metrics = TelemetryMetrics(**parsed)
                    loaded = True
            except Exception as e:
                print(f"Failed to initialize metrics from Redis: {e}")
                
        # 2. Try MongoDB if not found in Redis
        if not loaded and self._collection is not None:
            try:
                doc = await self._collection.find_one({"_id": "global_metrics"})
                if doc:
                    doc.pop("_id", None)
                    self._metrics = TelemetryMetrics(**doc)
                    loaded = True
            except Exception as e:
                print(f"Failed to initialize MongoDB metrics: {e}")
                
        # 3. Try local file fallback
        if not loaded and os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._metrics = TelemetryMetrics(**data)
                    loaded = True
            except Exception as e:
                print(f"Failed to initialize file metrics: {e}")
            
        # Start background sync task
        self._sync_task = asyncio.create_task(self._sync_loop())

    async def shutdown(self):
        """Ensures final metrics are flushed on shutdown."""
        if self._sync_task:
            self._sync_task.cancel()
        if self._dirty:
            await self._flush_to_db()

    async def _flush_to_db(self):
        """Writes current metrics to Redis, MongoDB, and local file."""
        async with self._lock:
            data = self._metrics.model_dump()
            self._dirty = False

        # 1. Flush to Redis
        if self._redis_client is not None:
            try:
                await self._redis_client.set("lites:global_metrics", json.dumps(data))
            except Exception as e:
                print(f"Failed to flush metrics to Redis: {e}")

        # 2. Flush to MongoDB
        if self._collection is not None:
            try:
                await self._collection.update_one(
                    {"_id": "global_metrics"},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                print(f"Failed to flush metrics to MongoDB: {e}")
                self._dirty = True

        # 3. Flush to local file
        try:
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    async def set_metrics(self, new_metrics: TelemetryMetrics):
        """Overrides the current metrics (e.g. for initial seeding) and flushes immediately."""
        async with self._lock:
            self._metrics = new_metrics.model_copy()
            self._dirty = True
        await self._flush_to_db()

    async def _sync_loop(self):
        """Background task that flushes metrics every 5 seconds if dirty."""
        while True:
            await asyncio.sleep(5)
            if self._dirty:
                await self._flush_to_db()

    async def record_request(self):
        async with self._lock:
            self._metrics.total_requests += 1
            self._dirty = True
            
    async def record_exact_cache_hit(self):
        async with self._lock:
            self._metrics.exact_cache_hits += 1
            self._dirty = True
            
    async def record_exact_cache_miss(self):
        async with self._lock:
            self._metrics.exact_cache_misses += 1
            self._dirty = True
            
    async def record_semantic_cache_hit(self):
        async with self._lock:
            self._metrics.semantic_cache_hits += 1
            self._dirty = True
            
    async def record_semantic_cache_miss(self):
        async with self._lock:
            self._metrics.semantic_cache_misses += 1
            self._dirty = True
            
    async def record_tokens_processed(self, tokens: int):
        async with self._lock:
            self._metrics.total_tokens_processed += tokens
            self._dirty = True

    async def record_rule_savings(self, tokens: int):
        async with self._lock:
            self._metrics.tokens_saved_by_rules += max(0, tokens)
            self._dirty = True
            
    async def record_ai_savings(self, tokens: int):
        async with self._lock:
            self._metrics.tokens_saved_by_ai += max(0, tokens)
            self._dirty = True
            
    async def record_overhead(self, ms: int):
        async with self._lock:
            self._metrics.total_optimization_overhead_ms += ms
            self._dirty = True
            
    async def record_provider_latency(self, ms: int):
        async with self._lock:
            self._metrics.provider_latency_ms += ms
            self._dirty = True
            
    async def record_total_latency(self, ms: int):
        async with self._lock:
            self._metrics.total_latency_ms += ms
            self._dirty = True
            
    async def record_cost_saved(self, cost: float):
        async with self._lock:
            self._metrics.total_estimated_cost_saved += max(0.0, cost)
            self._dirty = True
            
    async def record_routing_redirect(self):
        async with self._lock:
            self._metrics.total_routing_redirects += 1
            self._dirty = True
            
    def get_metrics(self) -> TelemetryMetrics:
        # Return a copy to avoid external mutation
        return self._metrics.model_copy()
