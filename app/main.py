from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.api.v1.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
