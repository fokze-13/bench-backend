from typing import Any
from app.schemas.event import SendMessageEvent, UserTypingEvent, WebSocketEvent
from pydantic import TypeAdapter

AnyClientEvent = SendMessageEvent | UserTypingEvent

_adapter: TypeAdapter = TypeAdapter(AnyClientEvent)


def serialize_client_event(raw_python_obj: dict[str, Any]) -> AnyClientEvent:
    return _adapter.validate_python(raw_python_obj)


def deserialize_event(event_obj: WebSocketEvent) -> dict[str, Any]:
    return event_obj.model_dump()
