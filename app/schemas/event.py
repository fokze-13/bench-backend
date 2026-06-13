from typing import Literal, Union
from pydantic import BaseModel
from app.schemas.payload import (
    SendMessagePayload,
    ReceiveMessagePayload,
    UserStatusPayload,
    ServerTypingPayload,
    ErrorPayload,
    UserTypingPayload,
)


class SendMessageEvent(BaseModel):
    event_type: Literal["send_message"] = "send_message"
    payload: SendMessagePayload


class ReceiveMessageEvent(BaseModel):
    event_type: Literal["receive_message"] = "receive_message"
    payload: ReceiveMessagePayload


class UserStatusEvent(BaseModel):
    event_type: Literal["user_status"] = "user_status"
    payload: UserStatusPayload


class UserTypingEvent(BaseModel):
    event_type: Literal["user_typing"] = "user_typing"
    payload: UserTypingPayload


class ServerTypingEvent(BaseModel):
    event_type: Literal["server_typing"] = "server_typing"
    payload: ServerTypingPayload


class ErrorEvent(BaseModel):
    event_type: Literal["error"] = "error"
    payload: ErrorPayload


class PingEvent(BaseModel):
    event_type: Literal["ping"] = "ping"


class PongEvent(BaseModel):
    event_type: Literal["pong"] = "pong"


WebSocketEvent = Union[
    SendMessageEvent,
    ReceiveMessageEvent,
    UserStatusEvent,
    ServerTypingEvent,
    UserTypingEvent,
    ErrorEvent,
    PingEvent,
    PongEvent,
]
