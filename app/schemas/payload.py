from typing import LiteralString
from pydantic import BaseModel
from app.config import USER_JOINED, USER_LEFT, STOP_TYPING, START_TYPING


class SendMessagePayload(BaseModel):
    message: str


class ReceiveMessagePayload(BaseModel):
    message: str
    alias: str


class UserStatusPayload(BaseModel):
    alias: str
    active_connections: int
    status: LiteralString[USER_JOINED, USER_LEFT]


class TypingPayload(BaseModel):
    typing: LiteralString[START_TYPING, STOP_TYPING]
    alias: str


class ErrorPayload(BaseModel):
    error_message: str
