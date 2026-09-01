import math
from typing import Optional, List, Tuple
from app.cache.models import CacheEntry
from app.config.env import env

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
        
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)

class InMemorySemanticCache:
    def __init__(self, threshold: Optional[float] = None):
        self.threshold = threshold if threshold is not None else env.SEMANTIC_CACHE_THRESHOLD
        # Store as list of tuples (embedding, target_model, CacheEntry)
        self._store: List[Tuple[List[float], str, CacheEntry]] = []
        
    async def search(self, embedding: List[float], target_model: str) -> Optional[CacheEntry]:
        """
        Searches the cache for the most semantically similar entry for the same model.
        Returns the entry if similarity > threshold.
        """
        if not embedding:
            return None
            
        best_score = -1.0
        best_entry = None
        
        # Clean up expired entries while iterating
        active_store = []
        
        for stored_emb, stored_model, entry in self._store:
            if entry.is_expired:
                continue
                
            active_store.append((stored_emb, stored_model, entry))
            
            # Segment by model
            if stored_model != target_model:
                continue
                
            score = cosine_similarity(embedding, stored_emb)
            if score > best_score:
                best_score = score
                best_entry = entry
                
        # Update store (removes expired)
        self._store = active_store
        
        if best_score >= self.threshold:
            return best_entry
            
        return None

    async def store(self, embedding: List[float], target_model: str, entry: CacheEntry) -> None:
        """Stores a new embedding and its corresponding cache entry."""
        if embedding:
            self._store.append((embedding, target_model, entry))
            
    async def clear(self) -> None:
        self._store.clear()
