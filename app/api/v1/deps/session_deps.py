from typing import Annotated
from fastapi import Depends
from redis.asyncio import Redis
from app.repositories.session_repo import SessionRepository
from app.services.session_service import SessionService

redis_client: Redis | None = None


async def get_redis() -> Redis | None:
    return redis_client


async def get_session_repo(
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> SessionRepository:
    return SessionRepository(redis_client)


async def get_session_service(
    service_repo: Annotated[SessionRepository, Depends(get_session_repo)],
) -> SessionService:
    return SessionService(service_repo)
