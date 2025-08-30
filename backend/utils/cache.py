import redis
import os

REDIS_URL = os.getenv("REDIS_URL")
_client = None

def get_redis_client():
    global _client
    if _client is None:
        _client = redis.from_url(REDIS_URL)
    return _client