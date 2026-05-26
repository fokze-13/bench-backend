from pydantic import BaseModel
from app.annotations import DeviceID, Token


class TokenCreate(BaseModel):
    device_id: DeviceID


class TokenRead(BaseModel):
    token: Token
