from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps.db_deps import get_session
from app.repositories.language_repo import LanguageRepository
from app.services.language_service import LanguageService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_language_repo(session: SessionDep) -> LanguageRepository:
    return LanguageRepository(session)


def get_language_service(
    repository: Annotated[LanguageRepository, Depends(get_language_repo)],
) -> LanguageService:
    return LanguageService(repository)
