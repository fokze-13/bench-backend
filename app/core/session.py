from dataclasses import dataclass
from typing import Optional
from enum import Enum


class SessionStatus(Enum):
    IDLE = "idle"
    MATCHED = "matched"
    CONNECTED = "connected"


@dataclass
class Session:
    sid: str
    token_ver: int
    room_id: Optional[str] = None
    status: str = SessionStatus.IDLE
