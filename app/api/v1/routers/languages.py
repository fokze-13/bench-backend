import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps.language_deps import get_language_service
from app.schemas.language import LanguagesMap
from app.services.language_service import LanguageService
from app.logger import setup_logger

router = APIRouter(prefix="/languages")

LanguageServiceDep = Annotated[LanguageService, Depends(get_language_service)]

logger = setup_logger(__name__, logging.DEBUG)


@router.get("/get_all", response_model=LanguagesMap)
async def get_all(language_service: LanguageServiceDep):
    try:
        return await language_service.get_all()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")
