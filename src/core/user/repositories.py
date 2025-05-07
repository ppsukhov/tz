from abc import ABC, abstractmethod

from core.user.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, item_id: User.ID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update(self, item_id: User.ID, data: dict) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, item_id: User.ID) -> bool:
        raise NotImplementedError
