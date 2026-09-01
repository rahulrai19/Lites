from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class CacheEntry(BaseModel):
    response: Any
    model: str
    timestamp: datetime
    ttl_seconds: Optional[int] = None
    
    @property
    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        delta = datetime.now() - self.timestamp
        return delta.total_seconds() > self.ttl_seconds
