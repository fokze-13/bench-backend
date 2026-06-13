from typing import Union
from app.schemas.event import (
    SendMessageEvent,
    ReceiveMessageEvent,
    UserStatusEvent,
    ErrorEvent,
    ServerTypingEvent,
    PingEvent,
    PongEvent, UserTypingEvent,
)

type DeviceID = str
type UserID = int
type SessionID = str

type Token = str
type JWTSecret = str

type DatabaseURL = str
type DatabaseHost = str
type DatabasePassword = str
type DatabaseUser = str
type DatabaseName = str

type RedisURL = str
type RedisPassword = str

type WebSocketEvent = Union[
    SendMessageEvent,
    ReceiveMessageEvent,
    UserStatusEvent,
    ServerTypingEvent,
    UserTypingEvent,
    ErrorEvent,
    PingEvent,
    PongEvent,
]
