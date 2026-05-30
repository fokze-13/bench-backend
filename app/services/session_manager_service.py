from app.annotations import DeviceID, SessionID
from app.core.connections import ConnectionManager
from app.repositories.session_repo import SessionRepository
from app.config import SessionUserStatus
from fastapi import WebSocket


class SessionManagerService:
    def __init__(
        self, redis_repository: SessionRepository, connection_manager: ConnectionManager
    ) -> None:
        self._redis_repo = redis_repository
        self._conn_manager = connection_manager

    async def connect_to_session(
        self, device_id: DeviceID, session_id: SessionID, websocket: WebSocket
    ) -> None:
        await self._conn_manager.connect(device_id, websocket)
        await self._redis_repo.update_session_user_status(
            session_id, device_id, str(SessionUserStatus.CONNECTED)
        )

    async def broadcast_message_in_session(
        self, device_id: DeviceID, session_id: SessionID, message: str
    ) -> None:
        session_users = await self._redis_repo.get_session_users(session_id)

        filtered_session_users = self._filter_session_users(
            session_users, own_device_id=device_id
        )

        await self._conn_manager.send_to(*filtered_session_users, message=message)

    async def disconnect_from_session(self, device_id: DeviceID, session_id: SessionID):
        await self._conn_manager.disconnect(device_id)
        await self._redis_repo.delete_session_user(session_id, device_id)

    @staticmethod
    def _filter_session_users(
        session_users: dict[DeviceID, SessionUserStatus], own_device_id: DeviceID
    ) -> list[DeviceID]:
        filtered = []

        for device_id, status in session_users.items():
            if device_id == own_device_id or status != str(SessionUserStatus.CONNECTED):
                continue
            filtered.append(device_id)

        return filtered
