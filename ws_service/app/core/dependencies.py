from functools import lru_cache

from app.services.ws import WebsocketService
from fastapi import Depends
from redis.asyncio import Redis


redis: Redis | None = None


@lru_cache
def get_redis() -> Redis | None:
    """Return Redis app instance."""
    return redis


@lru_cache()
def get_ws_service(redis: Redis = Depends(get_redis)) -> WebsocketService:
    """Return WebsocketService instance."""
    return WebsocketService(redis=redis)
