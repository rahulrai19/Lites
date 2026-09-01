from abc import ABC, abstractmethod
from typing import Optional
from app.cache.models import CacheEntry

class CacheProvider(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[CacheEntry]:
        """Retrieve an entry from the cache by key."""
        pass

    @abstractmethod
    async def set(self, key: str, entry: CacheEntry) -> None:
        """Store an entry in the cache by key."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Remove an entry from the cache by key."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all entries from the cache."""
        pass
