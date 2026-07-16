import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps.theme_deps import get_session_theme_service
from app.schemas.session_theme import ThemesMap
from app.services.session_theme_service import SessionThemeService
from app.logger import setup_logger

router = APIRouter(prefix="/session_themes")

SessionThemeServiceDep = Annotated[
    SessionThemeService, Depends(get_session_theme_service)
]

logger = setup_logger(__name__, logging.DEBUG)


@router.get("/get_all", response_model=ThemesMap)
async def get_all(session_theme_service: SessionThemeServiceDep):
    try:
        return await session_theme_service.get_all()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")
