"""
Cost Guard — Kiểm tra budget ngày dựa trên Redis.
Sử dụng sliding window hàng ngày để theo dõi chi phí.
"""
import time
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)


def check_budget(user_id: str):
    """Kiểm tra budget ngày từ Redis."""
    today = time.strftime("%Y-%m-%d")
    key = f"cost:{today}:{user_id}"

    current_cost = float(r.get(key) or 0)
    if current_cost >= settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail=f"Daily budget exceeded. Limit: ${settings.daily_budget_usd}/day."
        )


def record_usage(user_id: str, input_tokens: int, output_tokens: int):
    """Ghi nhận chi phí dùng đơn giá từ Config."""
    today = time.strftime("%Y-%m-%d")
    key = f"cost:{today}:{user_id}"

    cost = (input_tokens / 1000) * settings.price_per_1k_input + \
           (output_tokens / 1000) * settings.price_per_1k_output
    r.incrbyfloat(key, cost)
    r.expire(key, 86400)  # TTL = 1 day
