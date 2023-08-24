from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base


class AbstractRepository(ABC):
    model: type[Base]
    session = AsyncSession

    @abstractmethod
    async def add_new(self, data: dict) -> type[Base]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def patch_one(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def del_one(self, any: UUID) -> int:
        raise NotImplementedError
