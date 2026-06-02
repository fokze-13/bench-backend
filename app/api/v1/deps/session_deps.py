from typing import Annotated
from fastapi.params import Header, Query
from redis.asyncio import Redis
from app.annotations import DeviceID, Token, SessionID
from app.core.security import verify_token
from app.core.connections import ConnectionManager
from app.repositories.session_repo import SessionRepository
from app.services.session_manager_service import SessionManagerService
from app.services.session_search_service import SessionSearchService
from fastapi import Depends, HTTPException
from app.exceptions import InvalidToken
from fastapi import WebSocketException, status

redis_client: Redis | None = None
connection_manager: ConnectionManager | None = None


def get_redis() -> Redis | None:
    return redis_client


def get_connection_manager() -> ConnectionManager | None:
    return connection_manager


def get_session_repo(
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> SessionRepository:
    return SessionRepository(redis_client)


def get_session_search_service(
    session_repo: Annotated[SessionRepository, Depends(get_session_repo)],
) -> SessionSearchService:
    return SessionSearchService(session_repo)


def get_session_manager_service(
    session_repo: Annotated[SessionRepository, Depends(get_session_repo)],
    conn_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
) -> SessionManagerService:
    return SessionManagerService(
        redis_repository=session_repo, connection_manager=conn_manager
    )

def get_device_id(token: Annotated[Token, Header(...)]) -> DeviceID:
    try:
        device_id = verify_token(token)
        return device_id
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid token")


def websocket_get_session_id(
    session_id: SessionID = Query(...),  # type: ignore[assignment]
) -> SessionID:
    return session_id


def websocket_get_device_id(
    token: Token = Query(...),  # type: ignore[assignment]
) -> DeviceID:
    try:
        device_id = verify_token(token)
        return device_id
    except InvalidToken:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
