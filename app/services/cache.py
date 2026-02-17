import json
import redis
from typing import Any, Optional
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(str(settings.REDIS_URL))

    def get(self, key: str) -> Optional[Any]:
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, expire_seconds: int = 300):
        self.redis_client.set(key, json.dumps(value), ex=expire_seconds)

    def delete(self, key: str):
        self.redis_client.delete(key)

cache_service = CacheService()
