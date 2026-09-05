import json
import redis.asyncio as redis
from typing import Optional, List, Tuple
from app.cache.provider import CacheProvider
from app.cache.models import CacheEntry
from app.cache.semantic import cosine_similarity
from app.config.env import env

class RedisCache(CacheProvider):
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url)
        self.hits = 0
        self.misses = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    async def get(self, key: str) -> Optional[CacheEntry]:
        try:
            data = await self.client.get(f"exact:{key}")
        except Exception:
            # Simulate failure isolation
            self.misses += 1
            return None
            
        if data:
            entry = CacheEntry.model_validate_json(data)
            if entry.is_expired:
                self.misses += 1
                await self.delete(key)
                return None
            self.hits += 1
            return entry
            
        self.misses += 1
        return None

    async def set(self, key: str, entry: CacheEntry) -> None:
        # Use SETEX to natively handle TTL in Redis
        ttl = env.CACHE_TTL_SECONDS
        await self.client.setex(
            f"exact:{key}", 
            ttl, 
            entry.model_dump_json()
        )

    async def delete(self, key: str) -> None:
        await self.client.delete(f"exact:{key}")

    async def clear(self) -> None:
        # Warning: This is a simplistic clear for local dev.
        # In production, you'd probably want to use SCAN and pipelined deletes.
        keys = await self.client.keys("exact:*")
        if keys:
            await self.client.delete(*keys)

class RedisSemanticCache:
    def __init__(self, redis_url: str, threshold: Optional[float] = None):
        self.client = redis.from_url(redis_url)
        self.threshold = threshold if threshold is not None else env.SEMANTIC_CACHE_THRESHOLD

    async def search(self, embedding: List[float], target_model: str) -> Optional[CacheEntry]:
        """
        Searches the Redis cache by downloading all stored embeddings for the model
        and computing cosine similarity client-side.
        """
        if not embedding:
            return None

        # Fetch all hashes in the semantic namespace for this model
        hash_key = f"semantic:{target_model}"
        all_entries = await self.client.hgetall(hash_key)
        
        if not all_entries:
            return None

        best_score = -1.0
        best_entry = None
        expired_keys = []
        
        for k, v in all_entries.items():
            data = json.loads(v)
            entry = CacheEntry.model_validate_json(data["entry"])
            stored_emb = data["embedding"]
            
            if entry.is_expired:
                expired_keys.append(k)
                continue
                
            score = cosine_similarity(embedding, stored_emb)
            if score > best_score:
                best_score = score
                best_entry = entry

        # Cleanup expired entries asynchronously
        if expired_keys:
            await self.client.hdel(hash_key, *expired_keys)

        if best_score >= self.threshold:
            return best_entry
            
        return None

    async def store(self, embedding: List[float], target_model: str, entry: CacheEntry) -> None:
        import uuid
        if embedding:
            hash_key = f"semantic:{target_model}"
            
            # Generate a unique ID for this cache entry
            field_key = str(uuid.uuid4())
            
            data = {
                "embedding": embedding,
                "entry": entry.model_dump_json()
            }
            await self.client.hset(hash_key, field_key, json.dumps(data))

    async def clear(self) -> None:
        keys = await self.client.keys("semantic:*")
        if keys:
            await self.client.delete(*keys)
