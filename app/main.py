from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import UVICORN_LOGGING_CONFIG
from app.database import engine
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.session import router as session_router
from app.api.v1.routers.health_check import router as health_router
from app.config import settings
from app.redis_storage import get_redis_client
from app.api.v1.deps import session_deps
from app.core.connections import ConnectionManager
import logging.config

import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.config.dictConfig(UVICORN_LOGGING_CONFIG)
    logger.info("Starting up application...")
    session_deps.redis_client = await get_redis_client()
    session_deps.connection_manager = ConnectionManager()
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")
    await engine.dispose()
    await session_deps.redis_client.aclose()
    logger.info("Application shutdown complete")


app = FastAPI(
    lifespan=lifespan,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(health_router)
