from contextlib import asynccontextmanager
from typing import Any

from app.api.ws import router as api_router
from app.core import dependencies
from app.core.config import redis_settings, ws_service_settings
from fastapi import FastAPI
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> Any:
    """
    Open connections with dependent services.

    :param FastAPI _: FastAPI app instance.
    """
    dependencies.redis = Redis(**redis_settings.model_dump())
    yield
    await dependencies.redis.aclose()


app = FastAPI(
    title=ws_service_settings.name,
    lifespan=lifespan,
)

app.include_router(api_router)
