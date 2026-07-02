import pickle
import time
import uuid
from typing import Any, Dict, Tuple

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class CacheManager:
    """Server-side cache for credentials and events.

    Uses Redis when REDIS_URL is configured, otherwise falls back to an
    in-memory dict with TTL enforcement and periodic cleanup.
    """

    _in_memory_cache: Dict[str, Tuple[Any, float]] = {}  # key -> (value, expires_at)
    _redis_client = None
    _CLEANUP_THRESHOLD = 500  # run cleanup when cache exceeds this many entries

    @classmethod
    def init_redis(cls, redis_url: str = None, host: str = "localhost", port: int = 6379, db: int = 0):
        if not REDIS_AVAILABLE:
            return
        if redis_url:
            cls._redis_client = redis.from_url(redis_url)
        else:
            cls._redis_client = redis.Redis(host=host, port=port, db=db)

    @classmethod
    def store(cls, obj: Any, ttl: int = 3600) -> str:
        key = str(uuid.uuid4())
        if cls._redis_client:
            cls._redis_client.setex(key, ttl, pickle.dumps(obj))
        else:
            expires_at = time.monotonic() + ttl
            cls._in_memory_cache[key] = (obj, expires_at)
            if len(cls._in_memory_cache) > cls._CLEANUP_THRESHOLD:
                cls._cleanup()
        return key

    @classmethod
    def get(cls, key: str) -> Any | None:
        if not key:
            return None
        if cls._redis_client:
            val = cls._redis_client.get(key)
            return pickle.loads(val) if val else None
        entry = cls._in_memory_cache.get(key)
        if entry is None:
            return None
        obj, expires_at = entry
        if time.monotonic() > expires_at:
            cls._in_memory_cache.pop(key, None)
            return None
        return obj

    @classmethod
    def delete(cls, key: str):
        if cls._redis_client:
            cls._redis_client.delete(key)
        else:
            cls._in_memory_cache.pop(key, None)

    @classmethod
    def _cleanup(cls):
        """Remove all expired entries from the in-memory cache."""
        now = time.monotonic()
        expired = [k for k, (_, exp) in cls._in_memory_cache.items() if now > exp]
        for k in expired:
            cls._in_memory_cache.pop(k, None)
