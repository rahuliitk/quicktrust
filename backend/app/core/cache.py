"""Async Redis cache helper with graceful degradation.

When the Redis server is unreachable every public function silently
becomes a no-op so callers never need to guard against ``None`` or
exceptions from the cache layer.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import redis.asyncio as aioredis

from app.config import get_settings

logger = logging.getLogger(__name__)

_pool: aioredis.Redis | None = None
_available: bool | None = None  # ``None`` == not yet probed


async def _get_redis() -> aioredis.Redis | None:
    """Return a shared async Redis connection, or ``None`` if unavailable."""
    global _pool, _available

    if _available is False:
        return None

    if _pool is not None and _available is True:
        return _pool

    settings = get_settings()
    try:
        _pool = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
        )
        # Smoke-test the connection
        await _pool.ping()
        _available = True
        logger.info("Redis connected at %s", settings.REDIS_URL)
        return _pool
    except Exception as exc:
        logger.warning("Redis unavailable (%s). Caching will be disabled.", exc)
        _available = False
        _pool = None
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def cache_get(key: str) -> Any | None:
    """Retrieve a cached value by *key*.

    Returns ``None`` on cache miss **and** when Redis is unavailable.
    """
    r = await _get_redis()
    if r is None:
        return None

    try:
        raw = await r.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw
    except Exception as exc:
        logger.warning("cache_get(%s) failed: %s", key, exc)
        return None


async def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    """Store *value* under *key* with a TTL in seconds (default 5 min).

    No-op when Redis is unavailable.
    """
    r = await _get_redis()
    if r is None:
        return

    try:
        serialized = json.dumps(value) if not isinstance(value, str) else value
        await r.set(key, serialized, ex=ttl)
    except Exception as exc:
        logger.warning("cache_set(%s) failed: %s", key, exc)


async def cache_delete(key: str) -> None:
    """Delete a single cache key. No-op when Redis is unavailable."""
    r = await _get_redis()
    if r is None:
        return

    try:
        await r.delete(key)
    except Exception as exc:
        logger.warning("cache_delete(%s) failed: %s", key, exc)


async def cache_invalidate_pattern(pattern: str) -> int:
    """Delete all keys matching a glob *pattern* (e.g. ``org:*:controls``).

    Returns the number of keys deleted, or ``0`` when Redis is unavailable.

    Uses ``SCAN`` internally to avoid blocking the server with ``KEYS``.
    """
    r = await _get_redis()
    if r is None:
        return 0

    deleted = 0
    try:
        async for key in r.scan_iter(match=pattern, count=200):
            await r.delete(key)
            deleted += 1
    except Exception as exc:
        logger.warning("cache_invalidate_pattern(%s) failed: %s", pattern, exc)

    return deleted
