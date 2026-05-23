from app.repositories.user_repo import UserRepository
from app.services.abc_service import AbstractService
from app.types import DeviceID


class UserService(AbstractService):
    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def register(self, device_id: DeviceID) -> None:
        await self._repo.create(device_id=device_id)
