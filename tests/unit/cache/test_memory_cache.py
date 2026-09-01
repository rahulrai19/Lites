import pytest
from datetime import datetime, timedelta
from app.cache.memory import InMemoryCache
from app.cache.models import CacheEntry

@pytest.mark.asyncio
async def test_memory_cache_set_and_get():
    cache = InMemoryCache()
    entry = CacheEntry(
        response={"choices": [{"text": "Hello"}]},
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    await cache.set("test_key", entry)
    retrieved = await cache.get("test_key")
    
    assert retrieved is not None
    assert retrieved.model == "gpt-4o"
    assert retrieved.response["choices"][0]["text"] == "Hello"

@pytest.mark.asyncio
async def test_memory_cache_get_missing():
    cache = InMemoryCache()
    retrieved = await cache.get("missing_key")
    assert retrieved is None

@pytest.mark.asyncio
async def test_memory_cache_delete():
    cache = InMemoryCache()
    entry = CacheEntry(
        response={"text": "Hello"},
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    await cache.set("test_key", entry)
    await cache.delete("test_key")
    retrieved = await cache.get("test_key")
    
    assert retrieved is None

@pytest.mark.asyncio
async def test_memory_cache_clear():
    cache = InMemoryCache()
    entry = CacheEntry(
        response={"text": "Hello"},
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    await cache.set("key1", entry)
    await cache.set("key2", entry)
    await cache.clear()
    
    assert await cache.get("key1") is None
    assert await cache.get("key2") is None

@pytest.mark.asyncio
async def test_memory_cache_expiration():
    cache = InMemoryCache()
    # Create an entry that expired 10 seconds ago
    entry = CacheEntry(
        response={"text": "Hello"},
        model="gpt-4o",
        timestamp=datetime.now() - timedelta(seconds=10),
        ttl_seconds=5
    )
    
    await cache.set("test_key", entry)
    
    # Getting an expired entry should return None and delete it
    retrieved = await cache.get("test_key")
    assert retrieved is None
    
    # Verify it was deleted
    assert "test_key" not in cache._store
