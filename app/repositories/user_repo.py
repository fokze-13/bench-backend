from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.annotations import UserID, DeviceID


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: UserID) -> UserModel | None:
        user = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return user.scalar_one_or_none()

    async def get_by_device_id(self, device_id: DeviceID) -> UserModel | None:
        user = await self._session.execute(
            select(UserModel).where(UserModel.device_id == device_id)
        )
        return user.scalar_one_or_none()

    async def get_preferences_by_device_id(
        self, device_id: DeviceID
    ) -> UserModel | None:
        user = await self._session.execute(
            select(UserModel)
            .where(UserModel.device_id == device_id)
            .options(
                selectinload(UserModel.preferred_language),
                selectinload(UserModel.preferred_session_theme),
            )
        )
        return user.scalar_one_or_none()

    async def create(self, device_id: DeviceID) -> UserModel:
        new_user = UserModel(device_id=device_id)
        self._session.add(new_user)
        await self._session.flush()
        await self._session.refresh(new_user)

        return new_user

    async def update(self, user_id: UserID, **kwargs) -> None:
        await self._session.execute(
            update(UserModel).where(UserModel.id == user_id).values(**kwargs)
        )

    async def update_by_device_id(self, device_id: DeviceID, **kwargs) -> None:
        await self._session.execute(
            update(UserModel).where(UserModel.device_id == device_id).values(**kwargs)
        )

    async def delete(self, user_id: UserID) -> None:
        await self._session.execute(delete(UserModel).where(UserModel.id == user_id))

    async def delete_by_device_id(self, device_id: DeviceID) -> None:
        await self._session.execute(
            delete(UserModel).where(UserModel.device_id == device_id)
        )
