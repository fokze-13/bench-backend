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
)
from enum import Enum

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

    redis_url: RedisURL = env("REDIS_URL")


class SessionUserStatus(Enum):
    MATCHED = "matched"
    CONNECTED = "connected"


LOGGING_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGFILE = "logs/app.log"


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
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGFILE,
            "formatter": "default",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
    },
}

MAX_USERS_PER_SESSION = 3
SESSIONS_NAME = "sessions"
SESSION_USERS_NAME = "session:{session_id}"
SESSION_USERS_ALIASES_NAME = "session_aliases:{session_id}"


ERROR_MESSAGE_TYPE = "error"
EVENT_MESSAGE_TYPE = "event"
SEND_MESSAGE_TYPE = "send_message"
RECEIVE_MESSAGE_TYPE = "receive_message"


USER_ENTERED_CHAT = "{alias} entered the room"
USER_LEFT_CHAT = "{alias} left the room"


settings = Config()
