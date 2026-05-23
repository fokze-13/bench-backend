from pydantic import BaseModel
from app.types import DeviceID, Token


class TokenCreate(BaseModel):
    device_id: DeviceID


class TokenRead(BaseModel):
    token: Token
