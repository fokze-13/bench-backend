from pydantic import BaseModel


class MessageReceive(BaseModel):
    message: str


class MessageSend(BaseModel):
    message: str
    author_alias: str
