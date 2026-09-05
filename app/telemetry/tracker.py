from pydantic import BaseModel
import time
import asyncio
from typing import Optional
from pydantic import BaseModel

class TelemetryMetrics(BaseModel):
    total_requests: int = 0
    exact_cache_hits: int = 0
    semantic_cache_hits: int = 0
    tokens_saved_by_rules: int = 0
    tokens_saved_by_ai: int = 0
    total_optimization_overhead_ms: int = 0

class TelemetryTracker:
    def __init__(self, mongo_client=None):
        self._metrics = TelemetryMetrics()
        self._lock = asyncio.Lock()
        self._mongo_client = mongo_client
        self._collection = None
        self._sync_task = None
        self._dirty = False
        
        if self._mongo_client is not None:
            self._collection = self._mongo_client["lites"]["metrics"]

    async def initialize(self):
        """Loads historical metrics from MongoDB and starts the sync loop."""
        if self._collection is not None:
            try:
                doc = await self._collection.find_one({"_id": "global_metrics"})
                if doc:
                    doc.pop("_id", None)
                    self._metrics = TelemetryMetrics(**doc)
            except Exception as e:
                print(f"Failed to initialize MongoDB metrics: {e}")
            
            # Start background sync task regardless of initial load success
            self._sync_task = asyncio.create_task(self._sync_loop())

    async def shutdown(self):
        """Ensures final metrics are flushed on shutdown."""
        if self._sync_task:
            self._sync_task.cancel()
        if self._dirty:
            await self._flush_to_mongo()

    async def _flush_to_mongo(self):
        """Writes current metrics to MongoDB."""
        if self._collection is not None:
            try:
                async with self._lock:
                    data = self._metrics.model_dump()
                    self._dirty = False
                    
                await self._collection.update_one(
                    {"_id": "global_metrics"},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                print(f"Failed to flush metrics to MongoDB: {e}")
                # Re-mark as dirty so it tries again next time
                self._dirty = True

    async def _sync_loop(self):
        """Background task that flushes metrics every 5 seconds if dirty."""
        while True:
            await asyncio.sleep(5)
            if self._dirty:
                await self._flush_to_mongo()

    async def record_request(self):
        async with self._lock:
            self._metrics.total_requests += 1
            self._dirty = True
            
    async def record_exact_cache_hit(self):
        async with self._lock:
            self._metrics.exact_cache_hits += 1
            self._dirty = True
            
    async def record_semantic_cache_hit(self):
        async with self._lock:
            self._metrics.semantic_cache_hits += 1
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
            
    def get_metrics(self) -> TelemetryMetrics:
        # Return a copy to avoid external mutation
        return self._metrics.model_copy()
