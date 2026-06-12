from typing import Annotated, Union

from pydantic import Field

from app.schemas.event import SendMessageEvent, ReceiveMessageEvent, UserStatusEvent, ErrorEvent, TypingEvent, \
    PingEvent, PongEvent


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
        TypingEvent,
        ErrorEvent,
        PingEvent,
        PongEvent
    ]
