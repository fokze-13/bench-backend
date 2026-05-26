from app.annotations import DeviceID, Token
import jwt
from app.config import settings
from app.exceptions import InvalidToken


def create_access_token(device_id: DeviceID) -> Token:
    payload = {"device_id": device_id}
    token = jwt.encode(
        payload=payload, algorithm=settings.jwt_algorithm, key=settings.jwt_secret
    )
    return token


def verify_token(token: Token) -> DeviceID:
    try:
        payload = jwt.decode(
            jwt=token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return payload["device_id"]
    except jwt.InvalidTokenError as e:
        raise InvalidToken(f"Invalid token: {e}")
