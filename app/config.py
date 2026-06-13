from pydantic_settings import BaseSettings
from environs import env


from app.annotations import (
    DatabaseName,
    DatabasePassword,
    DatabaseUser,
    DatabaseURL,
    DatabaseHost,
    JWTSecret,
    RedisURL,
    RedisPassword,
)
from enum import Enum, StrEnum

env.read_env()


class Config(BaseSettings):
    db_name: DatabaseName = env("DB_NAME")
    db_password: DatabasePassword = env("DB_PSWD")
    db_user: DatabaseUser = env("DB_USER")
    db_host: DatabaseHost = env("DB_HOST")
    db_url: DatabaseURL = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    )

    jwt_secret: JWTSecret = env("JWT_SECRET")
    jwt_algorithm: str = env("JWT_ALGORITHM")

    redis_password: RedisPassword = env("REDIS_PASSWORD")
    redis_host: str = env("REDIS_HOST")
    redis_url: RedisURL = f"redis://:{redis_password}@{redis_host}:6379"

    is_production: bool = env("PRODUCTION")


class SessionUserStatus(Enum):
    MATCHED = "matched"
    CONNECTED = "connected"


LOGGING_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": LOGGING_FORMAT, "datefmt": LOGGING_DATE_FORMAT}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

MAX_USERS_PER_SESSION = 3
SESSIONS_NAME = "sessions"
SESSION_USERS_NAME = "session:{session_id}"
SESSION_USERS_ALIASES_NAME = "session_aliases:{session_id}"


class UserStatus(StrEnum):
    USER_JOINED = "joined"
    USER_LEFT = "left"


class TypingStatus(StrEnum):
    START_TYPING = "start"
    STOP_TYPING = "stop"


settings = Config()
