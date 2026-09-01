import pytest
from datetime import datetime, timedelta
from app.cache.semantic import InMemorySemanticCache, cosine_similarity
from app.cache.models import CacheEntry

def test_cosine_similarity():
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    assert cosine_similarity(vec1, vec2) == 1.0
    
    vec3 = [0.0, 1.0, 0.0]
    assert cosine_similarity(vec1, vec3) == 0.0
    
    vec4 = [1.0, 1.0, 0.0]
    # Cosine of 45 degrees is ~0.707
    assert 0.70 < cosine_similarity(vec1, vec4) < 0.71

@pytest.mark.asyncio
async def test_semantic_cache_hit():
    cache = InMemorySemanticCache(threshold=0.90)
    
    entry = CacheEntry(
        response="This is a sorted array",
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    # Store with a specific embedding
    vec_stored = [0.1, 0.2, 0.3, 0.4]
    await cache.store(vec_stored, "gpt-4o", entry)
    
    # Search with a very similar embedding
    vec_query = [0.1, 0.21, 0.29, 0.4]
    
    result = await cache.search(vec_query, "gpt-4o")
    assert result is not None
    assert result.response == "This is a sorted array"

@pytest.mark.asyncio
async def test_semantic_cache_miss_below_threshold():
    cache = InMemorySemanticCache(threshold=0.95)
    
    entry = CacheEntry(
        response="This is a sorted array",
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    vec_stored = [1.0, 0.0, 0.0]
    await cache.store(vec_stored, "gpt-4o", entry)
    
    # Search with a completely different embedding
    vec_query = [0.0, 1.0, 0.0]
    
    result = await cache.search(vec_query, "gpt-4o")
    assert result is None

@pytest.mark.asyncio
async def test_semantic_cache_miss_different_model():
    cache = InMemorySemanticCache(threshold=0.90)
    
    entry = CacheEntry(
        response="This is a sorted array",
        model="gpt-4o",
        timestamp=datetime.now()
    )
    
    vec_stored = [1.0, 0.0, 0.0]
    await cache.store(vec_stored, "gpt-4o", entry)
    
    # Search with identical embedding, but targeting a different model
    vec_query = [1.0, 0.0, 0.0]
    
    result = await cache.search(vec_query, "claude-3.5-sonnet")
    assert result is None

@pytest.mark.asyncio
async def test_semantic_cache_skips_expired():
    cache = InMemorySemanticCache(threshold=0.90)
    
    entry = CacheEntry(
        response="Expired entry",
        model="gpt-4o",
        timestamp=datetime.now() - timedelta(seconds=10),
        ttl_seconds=5
    )
    
    vec_stored = [1.0, 0.0, 0.0]
    await cache.store(vec_stored, "gpt-4o", entry)
    
    result = await cache.search(vec_stored, "gpt-4o")
    assert result is None
