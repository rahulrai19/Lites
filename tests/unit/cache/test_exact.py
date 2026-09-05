import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
import json

from app.cache.models import CacheEntry
from app.cache.memory import InMemoryCache
from app.cache.redis_backend import RedisCache
from app.cache.provider import CacheProvider

@pytest.fixture
def memory_cache():
    return InMemoryCache()

@pytest.fixture
def redis_cache():
    # Mock redis behavior using AsyncMock
    cache = RedisCache("redis://localhost:6379")
    mock_client = AsyncMock()
    
    # Simple dictionary to back the mock Redis client
    store = {}
    
    async def mock_get(key):
        return store.get(key)
        
    async def mock_setex(key, ttl, value):
        store[key] = value
        
    async def mock_delete(*keys):
        for key in keys:
            if key in store:
                del store[key]
                
    async def mock_keys(pattern):
        # Simplistic keys mock
        return list(store.keys())
    
    mock_client.get.side_effect = mock_get
    mock_client.setex.side_effect = mock_setex
    mock_client.delete.side_effect = mock_delete
    mock_client.keys.side_effect = mock_keys
    
    cache.client = mock_client
    return cache

@pytest.fixture(params=["memory_cache", "redis_cache"])
def cache(request, memory_cache, redis_cache):
    if request.param == "memory_cache":
        return memory_cache
    return redis_cache

def create_entry(text="Hello", model="gpt-4o", ttl=60) -> CacheEntry:
    return CacheEntry(
        response={"choices": [{"text": text}]},
        model=model,
        timestamp=datetime.now(),
        ttl_seconds=ttl
    )

@pytest.mark.asyncio
async def test_first_request_miss(cache: CacheProvider):
    result = await cache.get("first_req")
    assert result is None
    if hasattr(cache, "misses"):
        assert cache.misses == 1
        assert cache.hits == 0

@pytest.mark.asyncio
async def test_same_request_hit(cache: CacheProvider):
    entry = create_entry()
    await cache.set("same_req", entry)
    
    result = await cache.get("same_req")
    assert result is not None
    assert result.model == entry.model
    if hasattr(cache, "hits"):
        assert cache.hits == 1

@pytest.mark.asyncio
async def test_different_request_miss(cache: CacheProvider):
    entry = create_entry()
    await cache.set("req_A", entry)
    
    result = await cache.get("req_B")
    assert result is None
    if hasattr(cache, "misses"):
        assert cache.misses == 1

@pytest.mark.asyncio
async def test_cache_overwrite(cache: CacheProvider):
    entry1 = create_entry(text="Version 1")
    entry2 = create_entry(text="Version 2")
    
    await cache.set("overwrite_key", entry1)
    await cache.set("overwrite_key", entry2)
    
    result = await cache.get("overwrite_key")
    assert result.response["choices"][0]["text"] == "Version 2"

@pytest.mark.asyncio
async def test_delete(cache: CacheProvider):
    entry = create_entry()
    await cache.set("del_key", entry)
    await cache.delete("del_key")
    
    assert await cache.get("del_key") is None

@pytest.mark.asyncio
async def test_clear(cache: CacheProvider):
    await cache.set("key1", create_entry())
    await cache.set("key2", create_entry())
    
    await cache.clear()
    
    assert await cache.get("key1") is None
    assert await cache.get("key2") is None

@pytest.mark.asyncio
async def test_expiration(cache: CacheProvider):
    # Expired entry (ttl=5, but created 10 seconds ago)
    entry = CacheEntry(
        response={"text": "Hello"},
        model="gpt-4o",
        timestamp=datetime.now() - timedelta(seconds=10),
        ttl_seconds=5
    )
    await cache.set("expired_key", entry)
    
    result = await cache.get("expired_key")
    assert result is None
    
    # Boundary: Still valid (created 4 seconds ago, ttl=5)
    valid_entry = CacheEntry(
        response={"text": "Hello"},
        model="gpt-4o",
        timestamp=datetime.now() - timedelta(seconds=4),
        ttl_seconds=5
    )
    await cache.set("valid_key", valid_entry)
    
    result2 = await cache.get("valid_key")
    assert result2 is not None

@pytest.mark.asyncio
async def test_statistics():
    cache = InMemoryCache()
    await cache.set("key1", create_entry())
    
    await cache.get("key1") # HIT
    await cache.get("key1") # HIT
    await cache.get("missing_key") # MISS
    
    assert cache.hits == 2
    assert cache.misses == 1
    assert cache.hit_rate == (2 / 3)

@pytest.mark.asyncio
async def test_concurrency(cache: CacheProvider):
    # Test setting and getting the same key concurrently
    entry = create_entry()
    await cache.set("concurrent_key", entry)
    
    results = await asyncio.gather(
        cache.get("concurrent_key"),
        cache.get("concurrent_key"),
        cache.get("concurrent_key"),
        cache.get("concurrent_key"),
        cache.get("concurrent_key")
    )
    
    # All should be HITs and return the same entry
    for res in results:
        assert res is not None
        assert res.model == "gpt-4o"

@pytest.mark.asyncio
async def test_error_handling_redis():
    # Specifically test Redis cache error handling (simulating storage failure)
    cache = RedisCache("redis://localhost:6379")
    
    class BrokenRedis:
        async def get(self, key):
            raise ConnectionError("Redis is down")
    
    cache.client = BrokenRedis()
    
    result = await cache.get("any_key")
    assert result is None
    assert cache.misses == 1
