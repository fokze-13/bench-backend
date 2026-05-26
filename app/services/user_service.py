from app.repositories.user_repo import UserRepository
from app.annotations import DeviceID, Token
from app.core.security import create_access_token


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def register(self, device_id: DeviceID) -> Token:
        user_or_none = await self._repo.get_by_device_id(device_id)

        if not user_or_none:
            await self._repo.create(device_id=device_id)

        token = create_access_token(device_id=device_id)

        return token
