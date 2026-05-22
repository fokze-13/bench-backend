from datetime import datetime, timedelta
from dataclasses import dataclass
from app.config import settings
import jwt
from app.exceptions.token_exceptions import InvalidTokenError, ExpiredTokenError


SECRET = settings.jwt_secret
ALGORITHM = "HS256"
TTL = timedelta(hours=2)


instance = jwt


@dataclass
class TokenPayload:
    sid: str
    ver: int
    exp: datetime


def create_token(sid: str, ver: int) -> str:
    exp = datetime.now() + TTL
    payload = {"sid": sid, "ver": ver, "exp": exp}
    return instance.encode(payload=payload, key=SECRET, alg=ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    try:
        decoded = instance.decode(token, key=SECRET, algorithms=set(ALGORITHM))

        return TokenPayload(
            sid=decoded["sid"],
            ver=decoded["int"],
            exp=decoded["exp"]
        )
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError("This token had expired")
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError(f"Invalid token: {e}")
