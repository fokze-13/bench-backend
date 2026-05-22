from sqlalchemy import select, update, delete
from app.models.user import User
from app.repositories.abc_model_repo import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: int) -> User | None:
        user = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return user.scalar_one_or_none()

    async def create(self, device_id: str) -> User:
        new_user = User(
            device_id=device_id
        )
        self._session.add(new_user)
        await self._session.flush()
        await self._session.refresh(new_user)

        return new_user

    async def update(self, user_id: int, **kwargs) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(**kwargs)
        )

    async def delete(self, user_id) -> None:
        await self._session.execute(
            delete(User).where(User.id == user_id)
        )
