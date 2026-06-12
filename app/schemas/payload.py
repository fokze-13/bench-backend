from typing import Literal
from pydantic import BaseModel


class SendMessagePayload(BaseModel):
    message: str


class ReceiveMessagePayload(BaseModel):
    message: str
    alias: str


class UserStatusPayload(BaseModel):
    alias: str
    active_connections: int
    status: Literal["joined", "left"]


class TypingPayload(BaseModel):
    typing: Literal["start", "stop"]
    alias: str


class ErrorPayload(BaseModel):
    error_message: str
