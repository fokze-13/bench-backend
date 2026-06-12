from typing import Any
from app.annotations import WebSocketEvent
from pydantic import TypeAdapter

_adapter = TypeAdapter(WebSocketEvent)


def serialize_event(raw_python_obj: dict[str, Any]) -> WebSocketEvent:
    return _adapter.validate_python(raw_python_obj)


def deserialize_event(event_obj: WebSocketEvent) -> dict[str, Any]:
    return event_obj.model_dump()
