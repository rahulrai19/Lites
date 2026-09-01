from typing import Optional, Dict
from app.cache.provider import CacheProvider
from app.cache.models import CacheEntry

class InMemoryCache(CacheProvider):
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}

    async def get(self, key: str) -> Optional[CacheEntry]:
        entry = self._store.get(key)
        if entry is None:
            return None
            
        if entry.is_expired:
            await self.delete(key)
            return None
            
        return entry

    async def set(self, key: str, entry: CacheEntry) -> None:
        self._store[key] = entry

    async def delete(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    async def clear(self) -> None:
        self._store.clear()
