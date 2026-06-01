from pydantic import BaseModel
from app.schemas.payload import (
    ReceiveMessagePayload,
    SendMessagePayload,
    ErrorPayload,
    ServerEventPayload,
)


class Message(BaseModel):
    type: str
    payload: (
        ReceiveMessagePayload | SendMessagePayload | ErrorPayload | ServerEventPayload
    )
