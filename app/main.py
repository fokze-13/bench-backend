from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.api.v1.routers.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
