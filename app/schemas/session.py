from pydantic import BaseModel
from app.annotations import Token, SessionID


class GetSession(BaseModel):
    session_id: SessionID


class SessionHeaders(BaseModel):
    token: Token
