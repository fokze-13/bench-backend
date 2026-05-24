from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.api.v1.routers.auth import router as auth_router
from app.redis_storage import get_redis_client
from app.api.v1.deps import session_deps


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_deps.redis_client = await get_redis_client()
    yield
    await engine.dispose()
    await session_deps.redis_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
