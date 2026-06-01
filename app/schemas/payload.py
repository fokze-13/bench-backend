from pydantic import BaseModel


class ReceiveMessagePayload(BaseModel):
    message: str


class SendMessagePayload(BaseModel):
    message: str
    author_alias: str


class ServerEventPayload(BaseModel):
    event_message: str


class ErrorPayload(BaseModel):
    error_message: str
