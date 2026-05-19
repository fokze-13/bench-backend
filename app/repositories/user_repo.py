from sqlalchemy import select, update, delete
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, name: str, balance: float = 0.0) -> None:
        new_user = User(name=name, balance=balance)
        self.session.add(new_user)
        await self.session.flush()

    async def update(
        self, user_id: int, name: str = None, balance: float = None
    ) -> None:
        values = {}
        if name:
            values["name"] = name
        if balance:
            values["balance"] = balance

        await self.session.execute(
            update(User).where(User.id == user_id).values(**values)
        )

    async def delete(self, user_id: int) -> None:
        await self.session.execute(delete(User).where(User.id == user_id))
