from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserRead, UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> None:
        await self.repo.create(name=data.name)

    async def get(self, user_id: int) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserRead.model_validate(user)
