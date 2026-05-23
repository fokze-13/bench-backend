from pydantic import BaseModel


class TokenCreate(BaseModel):
    device_id: str


class TokenRead(BaseModel):
    token: str
