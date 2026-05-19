from pydantic_settings import BaseSettings
from environs import env

env.read_env()

class Config(BaseSettings):
    db_name: str = env("DB_NAME")
    db_password: str = env("DB_PSWD")
    db_user: str = env("DB_USER")
    db_host: str = env("DB_HOST")
    db_url: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    )


settings = Config()
