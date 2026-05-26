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


settings = Config()
