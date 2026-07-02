from fastapi import APIRouter
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.session import router as session_router
from app.api.v1.routers.health_check import router as health_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(session_router)
router.include_router(health_router)
