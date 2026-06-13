from typing import Literal
from pydantic import BaseModel
from app.schemas.payload import (
    SendMessagePayload,
    ReceiveMessagePayload,
    UserStatusPayload,
    ServerTypingPayload,
    ErrorPayload, UserTypingPayload,
)


class SendMessageEvent(BaseModel):
    type: Literal["send_message"] = "send_message"
    payload: SendMessagePayload


class ReceiveMessageEvent(BaseModel):
    type: Literal["receive_message"] = "receive_message"
    payload: ReceiveMessagePayload


class UserStatusEvent(BaseModel):
    type: Literal["user_status"] = "user_status"
    payload: UserStatusPayload


class UserTypingEvent(BaseModel):
    type: Literal["user_typing"] = "user_typing"
    payload: UserTypingPayload


class ServerTypingEvent(BaseModel):
    type: Literal["server_typing"] = "server_typing"
    payload: ServerTypingPayload


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    payload: ErrorPayload


class PingEvent(BaseModel):
    type: Literal["ping"] = "ping"


class PongEvent(BaseModel):
    type: Literal["pong"] = "pong"
