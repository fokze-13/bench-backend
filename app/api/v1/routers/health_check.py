import logging
from typing import Annotated
from fastapi import APIRouter, status, Depends
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps.db_deps import get_session
from sqlalchemy import select
from app.config import settings
from fastapi.responses import JSONResponse
from app.logger import setup_logger

router = APIRouter(prefix="/health")
logger = setup_logger(__name__, logging.DEBUG)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", status_code=status.HTTP_200_OK, tags=["system"])
async def health(db_session: SessionDep):
    checks = {}

    try:
        await db_session.execute(select(1))
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {e}"
        logger.error(f"Postgres error: {e}")

    try:
        redis = aioredis.from_url(settings.redis_url)
        await redis.ping()  # type: ignore[misc]
        await redis.aclose()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"
        logger.error(f"Redis error: {e}")

    all_ok = all(v == "ok" for v in checks.values())
    status_code = status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
        },
    )
