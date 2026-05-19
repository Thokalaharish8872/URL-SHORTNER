import redis
import time
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    _instance = None
    _failed_until = 0

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            try:
                cls._instance = redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)
                # Test connection with timeout
                cls._instance.ping()
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                cls._instance = None
        return cls._instance

    @classmethod
    def get(cls, key: str):
        client = cls.get_client()
        if not client:
            return None
        try:
            return client.get(key)
        except Exception as e:
            logger.warning(f"Redis get failed for {key}: {e}")
            return None

    @classmethod
    def set(cls, key: str, value: str, ex: int = 3600):
        client = cls.get_client()
        if not client:
            return False
        try:
            client.set(key, value, ex=ex)
            return True
        except Exception as e:
            logger.warning(f"Redis set failed for {key}: {e}")
            return False

    @classmethod
    def delete(cls, key: str):
        client = cls.get_client()
        if not client:
            return False
        try:
            client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Redis delete failed for {key}: {e}")
            return False

    @classmethod
    def incr(cls, key: str, ex: int = None):
        client = cls.get_client()
        if not client:
            return None
        try:
            val = client.incr(key)
            if ex and val == 1:
                client.expire(key, ex)
            return val
        except Exception as e:
            logger.warning(f"Redis incr failed for {key}: {e}")
            return None
