from app.annotations import DeviceID, SessionID
from app.core.alias import generate_alias
from app.core.connections import ConnectionManager
from app.repositories.session_repo import SessionRepository
from app.config import SessionUserStatus, USER_ENTERED_CHAT, USER_LEFT_CHAT
from fastapi import WebSocket
from app.schemas.message import Message
from app.schemas.payload import (
    SendMessagePayload,
    ReceiveMessagePayload,
    ServerEventPayload,
)
from app.config import EVENT_MESSAGE_TYPE, RECEIVE_MESSAGE_TYPE, SEND_MESSAGE_TYPE
from typing import Any
import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)

# TODO maybe delegate the message logic to it's own module


class SessionManagerService:
    def __init__(
        self, redis_repository: SessionRepository, connection_manager: ConnectionManager
    ) -> None:
        self._redis_repo = redis_repository
        self._conn_manager = connection_manager

    async def connect_to_session(
        self, device_id: DeviceID, session_id: SessionID, websocket: WebSocket
    ) -> None:
        logger.info(f"Connecting device {device_id} to session {session_id}")
        await self._conn_manager.connect(device_id, websocket)
        await self._redis_repo.update_session_user_status(
            session_id, device_id, str(SessionUserStatus.CONNECTED)
        )

        session_users_count = await self._redis_repo.get_session_users_count(session_id)
        alias = generate_alias(session_users_count)

        await self._redis_repo.add_session_user_alias(session_id, device_id, alias)

        await self._broadcast_message_in_session(
            device_id=device_id,
            session_id=session_id,
            json_message=Message(
                type=EVENT_MESSAGE_TYPE,
                payload=ServerEventPayload(
                    event_message=USER_ENTERED_CHAT.format(alias=alias)
                ),
            ).model_dump(),
        )

    async def handle_message(
        self, device_id: DeviceID, session_id: SessionID, message: Message
    ) -> None:
        if message.type == RECEIVE_MESSAGE_TYPE:
            payload = message.payload
            await self._handle_user_received_message(
                device_id=device_id, session_id=session_id, payload=payload  # type: ignore[arg-type]
            )

    async def _handle_user_received_message(
        self, device_id: DeviceID, session_id: SessionID, payload: ReceiveMessagePayload
    ):
        alias = await self._redis_repo.get_session_user_alias(
            session_id=session_id, device_id=device_id
        )
        message_content = payload.message

        await self._broadcast_message_in_session(
            device_id=device_id,
            session_id=session_id,
            json_message=Message(
                type=SEND_MESSAGE_TYPE,
                payload=SendMessagePayload(message=message_content, author_alias=alias),
            ).model_dump(),
        )

    async def _broadcast_message_in_session(
        self, device_id: DeviceID, session_id: SessionID, json_message: dict[str, Any]
    ) -> None:
        logger.info(f"Broadcasting message in session {session_id} from device {device_id}")
        session_users = await self._redis_repo.get_session_users(session_id)

        filtered_session_users = self._filter_session_users(
            session_users, own_device_id=device_id
        )

        await self._conn_manager.send_to(
            *filtered_session_users, json_message=json_message
        )

    async def disconnect_from_session(
        self, device_id: DeviceID, session_id: SessionID
    ) -> None:
        logger.info(f"Disconnecting device {device_id} from session {session_id}")
        alias = await self._redis_repo.get_session_user_alias(
            session_id=session_id, device_id=device_id
        )

        await self._conn_manager.disconnect(device_id)
        await self._redis_repo.delete_session_user(session_id, device_id)
        await self._broadcast_message_in_session(
            device_id=device_id,
            session_id=session_id,
            json_message=Message(
                type=EVENT_MESSAGE_TYPE,
                payload=ServerEventPayload(
                    event_message=USER_LEFT_CHAT.format(alias=alias)
                ),
            ).model_dump(),
        )

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
