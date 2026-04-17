import time
import redis
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)


def _get_month_key(user_id: str):
    month = time.strftime("%Y-%m")
    return f"cost:{user_id}:{month}"


def check_budget(user_id: str):
    key = _get_month_key(user_id)

    current = r.get(key)
    current = float(current) if current else 0.0

    if current >= settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail="Monthly budget exceeded",
        )


def record_cost(user_id: str, input_tokens: int, output_tokens: int):
    key = _get_month_key(user_id)

    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006

    r.incrbyfloat(key, cost)