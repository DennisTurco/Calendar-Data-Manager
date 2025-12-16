import pickle
import uuid
from typing import Any, Dict
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class CacheManager:
    """Cache server-side for credentials and events"""
    _in_memory_cache: Dict[str, Any] = {}
    _redis_client = None

    @classmethod
    def init_redis(cls, host="localhost", port=6379, db=0):
        if REDIS_AVAILABLE:
            cls._redis_client = redis.Redis(host=host, port=port, db=db)

    @classmethod
    def store(cls, obj: Any, ttl: int = 3600) -> str:
        key = str(uuid.uuid4())
        if cls._redis_client:
            cls._redis_client.setex(key, ttl, pickle.dumps(obj))
        else:
            cls._in_memory_cache[key] = obj
        return key

    @classmethod
    def get(cls, key: str) -> Any | None:
        if cls._redis_client:
            val = cls._redis_client.get(key)
            return pickle.loads(val) if val else None
        return cls._in_memory_cache.get(key)

    @classmethod
    def delete(cls, key: str):
        if cls._redis_client:
            cls._redis_client.delete(key)
        else:
            cls._in_memory_cache.pop(key, None)
