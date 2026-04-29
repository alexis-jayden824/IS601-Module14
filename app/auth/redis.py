# app/auth/redis.py
import time

try:
    import redis.asyncio as redis_async
except Exception:
    redis_async = None

from app.core.config import get_settings

settings = get_settings()
_in_memory_blacklist = {}


def _purge_expired_tokens() -> None:
    now = time.time()
    expired = [jti for jti, expires_at in _in_memory_blacklist.items() if expires_at <= now]
    for jti in expired:
        _in_memory_blacklist.pop(jti, None)


async def get_redis():
    if not hasattr(get_redis, "redis"):
        get_redis.redis = None
        if redis_async is not None:
            try:
                candidate = redis_async.from_url(settings.REDIS_URL or "redis://localhost")
                await candidate.ping()
                get_redis.redis = candidate
            except Exception:
                get_redis.redis = None
    return get_redis.redis


async def add_to_blacklist(jti: str, exp: int):
    """Add a token's JTI to the blacklist."""
    if exp <= 0:
        return

    redis = await get_redis()
    if redis is not None:
        try:
            await redis.set(f"blacklist:{jti}", "1", ex=exp)
            return
        except Exception:
            pass

    _in_memory_blacklist[jti] = time.time() + exp
    _purge_expired_tokens()


async def is_blacklisted(jti: str) -> bool:
    """Check if a token's JTI is blacklisted."""
    redis = await get_redis()
    if redis is not None:
        try:
            return bool(await redis.exists(f"blacklist:{jti}"))
        except Exception:
            pass

    _purge_expired_tokens()
    return jti in _in_memory_blacklist