from abc import ABC, abstractmethod
from app.models.base import Base

class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, obj_id: int) -> Base | None:
        pass

    @abstractmethod
    async def create(self, **kwargs) -> Base:
        pass

    @abstractmethod
    async def update(self, obj_id: int, **kwargs) -> None:
        pass

    @abstractmethod
    async def delete(self, obj_id: int) -> None:
        pass