import json
from uuid import uuid4
from typing import Any
from redis.asyncio import Redis
from app.annotations import SessionID, DeviceID


class SessionRepository:
    _sessions_name = "sessions"
    _session_users_name = "session:{session_id}"

    def __init__(self, client: Redis) -> None:
        self._client = client

    async def get_sessions(self) -> set[SessionID]:
        sessions = await self._client.smembers(self._sessions_name)

        return sessions

    async def get_sessions_count(self) -> int:
        return await self._client.scard(self._sessions_name)

    async def get_session_users(self, session_id: SessionID) -> dict[str, Any]:
        info = await self._client.hgetall(
            self._session_users_name.format(session_id=session_id)
        )

        return info

    async def create_new_session(self) -> SessionID:
        session_id = str(uuid4())
        await self._client.sadd(self._sessions_name, session_id)

        return session_id

    async def get_session_users_count(self, session_id: SessionID) -> int:
        return await self._client.hlen(
            self._session_users_name.format(session_id=session_id)
        )

    async def get_session_user_status(
        self, session_id: SessionID, device_id: DeviceID
    ) -> str:
        return await self._client.hget(
            self._session_users_name.format(session_id=session_id), device_id
        )

    async def update_session_user_status(
        self, session_id: SessionID, device_id: DeviceID, status: str
    ) -> None:
        await self._client.hset(
            self._session_users_name.format(session_id=session_id),
            key=device_id,
            value=status,
        )

    async def delete_session_user(
        self, session_id: SessionID, device_id: DeviceID
    ) -> None:
        await self._client.hdel(
            self._session_users_name.format(session_id=session_id), device_id
        )
