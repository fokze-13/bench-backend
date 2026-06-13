from pydantic import BaseModel
from app.config import UserStatus, TypingStatus


class SendMessagePayload(BaseModel):
    message: str


class ReceiveMessagePayload(BaseModel):
    message: str
    alias: str


class UserStatusPayload(BaseModel):
    alias: str
    active_connections: int
    status: UserStatus


class UserTypingPayload(BaseModel):
    typing: TypingStatus


class ServerTypingPayload(BaseModel):
    typing: TypingStatus
    alias: str


class ErrorPayload(BaseModel):
    error_message: str
