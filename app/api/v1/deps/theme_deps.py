from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps.db_deps import get_session
from app.repositories.session_theme_repo import SessionThemeRepository
from app.services.session_theme_service import SessionThemeService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_session_theme_repo(session: SessionDep) -> SessionThemeRepository:
    return SessionThemeRepository(session)


def get_session_theme_service(
    repository: Annotated[SessionThemeRepository, Depends(get_session_theme_repo)],
) -> SessionThemeService:
    return SessionThemeService(repository)
