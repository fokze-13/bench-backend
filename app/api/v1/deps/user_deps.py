from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps.db_deps import get_session
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repository)
