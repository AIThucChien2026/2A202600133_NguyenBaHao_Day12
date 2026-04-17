import time
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)

def check_rate_limit(user_id: str):
    """Redis-based sliding window rate limiter."""
    now = time.time()
    key = f"rate_limit:{user_id}"
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - 60)
    pipe.zcard(key)
    pipe.zadd(key, {str(now): now})
    pipe.expire(key, 60)
    results = pipe.execute()
    
    count = results[1]
    if count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.rate_limit_per_minute} req/min."
        )
