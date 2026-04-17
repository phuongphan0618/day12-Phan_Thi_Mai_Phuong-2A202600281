import time
import redis
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)


def check_rate_limit(user_id: str):
    key = f"rate:{user_id}"
    now = int(time.time())

    # remove request cũ > 60s
    r.zremrangebyscore(key, 0, now - 60)

    # count current window
    count = r.zcard(key)

    if count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )

    # add new request
    r.zadd(key, {str(now): now})
    r.expire(key, 60)