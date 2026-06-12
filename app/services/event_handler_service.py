from app.schemas.event import (
    SendMessageEvent,
    ReceiveMessageEvent,
    UserStatusEvent,
    ErrorEvent,
    TypingEvent,
    PingEvent,
    PongEvent,
)
from app.annotations import WebSocketEvent
from typing import Protocol


class EventHandlerCallable(Protocol):
    async def __call__(self, event: WebSocketEvent) -> None: ...


class EventHandlerService:
    def __init__(self):
        self._handlers_match: dict[str, EventHandlerCallable] = {
            SendMessageEvent.type: self._send_message_event_handler,
            ReceiveMessageEvent.type: self._receive_message_event_handler,
            UserStatusEvent.type: self._user_status_event_handler,
            ErrorEvent.type: self._error_event_handler,
            TypingEvent.type: self._typing_event_handler,
            PingEvent.type: self._typing_event_handler,
            PongEvent.type: self._pong_event_handler,
        }

    async def handle(self, event: WebSocketEvent):
        handler = self._handlers_match[event.type]
        await handler(event)

    async def _send_message_event_handler(self, event: SendMessageEvent): ...

    async def _receive_message_event_handler(self, event: ReceiveMessageEvent): ...

    async def _user_status_event_handler(self, event: UserStatusEvent): ...

    async def _error_event_handler(self, event: ErrorEvent): ...

    async def _typing_event_handler(self, event: TypingEvent): ...

    async def _ping_event_handler(self, event: PingEvent): ...

    async def _pong_event_handler(self, event: PongEvent): ...
