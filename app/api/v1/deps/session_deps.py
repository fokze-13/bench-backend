from typing import Annotated
from fastapi import Depends
from fastapi.params import Header, Query
from redis.asyncio import Redis
from app.annotations import DeviceID, Token, SessionID
from app.core.security import verify_token
from app.repositories.session_repo import SessionRepository
from app.schemas.session import SessionQueryParams
from app.services.session_search_service import SessionSearchService

redis_client: Redis | None = None


async def get_redis() -> Redis | None:
    return redis_client


async def get_session_repo(
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> SessionRepository:
    return SessionRepository(redis_client)


async def get_session_search_service(
    service_repo: Annotated[SessionRepository, Depends(get_session_repo)],
) -> SessionSearchService:
    return SessionSearchService(service_repo)


async def get_device_id(token: Annotated[Token, Header(...)]) -> DeviceID:
    device_id = verify_token(token)
    return device_id


async def websocket_get_session_id(
    query: Annotated[SessionQueryParams, Query(...)],
) -> SessionID:
    session_id = query.session_id
    return session_id


async def websocket_get_device_id(
    query: Annotated[SessionQueryParams, Query(...)],
) -> DeviceID:
    device_id = verify_token(query.token)
    return device_id
