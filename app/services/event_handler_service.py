from app.core.serializer_helper import deserialize_event
from app.repositories.session_repo import SessionRepository
from app.schemas.event import (
    SendMessageEvent,
    ReceiveMessageEvent,
    ServerTypingEvent,
    UserTypingEvent,
)
from app.annotations import DeviceID, SessionID
from typing import Protocol, Literal, Any
from app.schemas.payload import ReceiveMessagePayload, ServerTypingPayload
from app.services.session_manager_service import SessionManagerService


class EventHandlerCallable(Protocol):
    async def __call__(
        self, event: Any, device_id: DeviceID, session_id: SessionID
    ) -> None: ...


class EventHandlerService:
    def __init__(
        self,
        redis_repository: SessionRepository,
        session_manager: SessionManagerService,
    ) -> None:
        self._redis_repo = redis_repository
        self._session_manager = session_manager

        self._handlers_match: dict[
            Literal["send_message", "user_typing"], EventHandlerCallable
        ] = {
            "send_message": self._send_message_event_handler,
            "user_typing": self._typing_event_handler,
        }

    async def handle(
        self,
        event: UserTypingEvent | SendMessageEvent,
        device_id: DeviceID,
        session_id: SessionID,
    ) -> None:
        handler = self._handlers_match[event.event_type]
        await handler(event, device_id, session_id)

    async def _send_message_event_handler(
        self, event: SendMessageEvent, device_id: DeviceID, session_id: SessionID
    ) -> None:
        message = event.payload.message
        alias = await self._redis_repo.get_session_user_alias(
            session_id=session_id, device_id=device_id
        )

        receive_message = ReceiveMessageEvent(
            payload=ReceiveMessagePayload(
                message=message,
                alias=alias,
            )
        )

        python_obj_message = deserialize_event(receive_message)

        await self._session_manager.broadcast_message_in_session(
            device_id=device_id,
            session_id=session_id,
            python_obj_message=python_obj_message,
        )

    async def _typing_event_handler(
        self, event: UserTypingEvent, device_id: DeviceID, session_id: SessionID
    ) -> None:
        event_status = event.payload.typing

        alias = await self._redis_repo.get_session_user_alias(
            device_id=device_id, session_id=session_id
        )

        server_event = ServerTypingEvent(
            payload=ServerTypingPayload(typing=event_status, alias=alias)
        )

        python_obj_method = deserialize_event(server_event)

        await self._session_manager.broadcast_message_in_session(
            device_id=device_id,
            session_id=session_id,
            python_obj_message=python_obj_method,
        )
