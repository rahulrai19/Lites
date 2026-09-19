import pytest
from app.cache.semantic import InMemorySemanticCache, cosine_similarity
from app.cache.models import CacheEntry
from datetime import datetime

# A Mock Embedder that returns exact vectors based on the query,
# allowing us to precisely control cosine similarity in the test environment.
class MockVectorEmbedder:
    async def get_embedding(self, text: str) -> list[float]:
        vectors = {
            "Explain Redis.": [1.0, 0.0, 0.0],
            "What is Redis?": [0.98, 0.198, 0.0],          # Cosine Sim: ~0.98 (Positive Match)
            "Can you explain Redis?": [0.96, 0.28, 0.0],   # Cosine Sim: ~0.96 (Positive Match)
            "How do I uninstall Redis?": [0.0, 1.0, 0.0],  # Cosine Sim: 0.0 (Negative)
            "How does Redis persistence work?": [0.5, 0.866, 0.0] # Cosine Sim: 0.5 (Negative)
        }
        return vectors.get(text, [0.0, 0.0, 1.0])

@pytest.fixture
def embedder():
    return MockVectorEmbedder()

@pytest.fixture
def cache():
    # Use standard 0.95 threshold as default for the cache
    return InMemorySemanticCache(threshold=0.95)

def create_entry(response: str = "Cached Response") -> CacheEntry:
    return CacheEntry(response=response, model="gpt-4o", metadata={"source": "test"}, timestamp=datetime.utcnow().isoformat())

@pytest.mark.asyncio
async def test_cosine_similarity_math():
    """Verify raw mathematical correctness of cosine_similarity function."""
    vec_a = [1.0, 0.0, 0.0]
    vec_b = [1.0, 0.0, 0.0]
    vec_c = [0.0, 1.0, 0.0]
    
    assert cosine_similarity(vec_a, vec_b) == 1.0
    assert cosine_similarity(vec_a, vec_c) == 0.0

@pytest.mark.asyncio
async def test_semantic_cache_evaluation(embedder, cache):
    """
    Test positive/negative cases using controlled embeddings.
    Measures and reports True Positives, True Negatives, False Positives, False Negatives.
    """
    base_query = "Explain Redis."
    
    positive_queries = [
        "What is Redis?",
        "Can you explain Redis?"
    ]
    
    negative_queries = [
        "How do I uninstall Redis?",
        "How does Redis persistence work?"
    ]
    
    # 1. Generate base embedding and store it in cache
    base_embedding = await embedder.get_embedding(base_query)
    entry = create_entry()
    cache._store.append((base_embedding, "gpt-4o", entry))
    
    # Tracking metrics
    tp, fn, tn, fp = 0, 0, 0, 0
    results_log = []
    
    # 2. Evaluate Positive Queries (Expect Hit / Score >= 0.95)
    for q in positive_queries:
        emb = await embedder.get_embedding(q)
        hit = await cache.search(emb, "gpt-4o")
        score = cosine_similarity(base_embedding, emb)
        
        results_log.append(f"[POS] '{q}' -> Score: {score:.3f}")
        if hit:
            tp += 1
        else:
            fn += 1
            
    # 3. Evaluate Negative Queries (Expect Miss / Score < 0.95)
    for q in negative_queries:
        emb = await embedder.get_embedding(q)
        hit = await cache.search(emb, "gpt-4o")
        score = cosine_similarity(base_embedding, emb)
        
        results_log.append(f"[NEG] '{q}' -> Score: {score:.3f}")
        if not hit:
            tn += 1
        else:
            fp += 1

    # Print Report for Verification
    print("\n--- Semantic Cache Evaluation Report ---")
    for log in results_log:
        print(log)
    print(f"\nTP: {tp} | FN: {fn}")
    print(f"TN: {tn} | FP: {fp}")
    print("----------------------------------------")

    # Critical Requirement: False positives are dangerous!
    assert fp == 0, "DANGER: Semantic cache falsely matched distinct intents!"
    assert tp == 2, "Failed to match valid positive cases!"
    assert tn == 2, "Failed to correctly reject negative cases!"
    
@pytest.mark.asyncio
async def test_boundary_cases():
    """
    Test exact boundary handling: threshold - epsilon, threshold, threshold + epsilon.
    """
    cache_boundary = InMemorySemanticCache(threshold=0.85)
    base_emb = [1.0, 0.0]
    
    # Boundary exactly at threshold (0.85)
    cache_boundary._store = [(base_emb, "gpt-4o", create_entry("Exact"))]
    exact_hit = await cache_boundary.search([0.85, 0.52678268764], "gpt-4o")
    
    # Epsilon above (0.86)
    cache_boundary._store = [(base_emb, "gpt-4o", create_entry("Above"))]
    above_hit = await cache_boundary.search([0.86, 0.51029403288], "gpt-4o")
    
    # Epsilon below (0.84)
    cache_boundary._store = [(base_emb, "gpt-4o", create_entry("Below"))]
    below_hit = await cache_boundary.search([0.84, 0.54258658295], "gpt-4o")
    
    assert exact_hit is not None
    assert above_hit is not None
    assert below_hit is None
