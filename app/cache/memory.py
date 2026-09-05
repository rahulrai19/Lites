from typing import Optional, Dict
from app.cache.provider import CacheProvider
from app.cache.models import CacheEntry

class InMemoryCache(CacheProvider):
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    async def get(self, key: str) -> Optional[CacheEntry]:
        entry = self._store.get(key)
        if entry is None:
            self.misses += 1
            return None
            
        if entry.is_expired:
            self.misses += 1
            await self.delete(key)
            return None
            
        self.hits += 1
        return entry

    async def set(self, key: str, entry: CacheEntry) -> None:
        self._store[key] = entry

    async def delete(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    async def clear(self) -> None:
        self._store.clear()
