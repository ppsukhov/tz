from advanced_alchemy import repository
from advanced_alchemy.exceptions import NotFoundError
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.user.entities import User
from core.user.repositories import UserRepository
from infra.db.models import UserModel


class DBUserRepository(repository.SQLAlchemyAsyncRepository[UserModel], UserRepository):
    model_type = UserModel

    def __init__(self, db_session: AsyncSession):
        super().__init__(session=db_session)

    async def find_by_id(self, item_id: User.ID) -> User | None:
        try:
            db_item = await self.get(item_id=item_id)
            return User.model_construct(**db_item.__dict__)
        except NotFoundError:
            return

    async def get_all(self) -> list[User]:
        db_items = await self.list()
        return [User.model_construct(**d.__dict__) for d in db_items]

    async def create(self, data: dict) -> User:
        db_item = await self.add(UserModel(**data), auto_commit=True)
        return User.model_construct(**db_item.__dict__)

    async def update(self, item_id: User.ID, data: dict) -> User | None:
        db_item = await self.find_by_id(item_id)
        if not db_item:
            return

        db_item = await super().update(
            UserModel(**db_item.__dict__ | data),
            attribute_names=data.keys(),
            auto_commit=True,
        )
        return User.model_construct(**db_item.__dict__)

    async def delete_by_id(self, item_id: User.ID) -> bool:
        try:
            await self.delete(item_id=item_id)
            return True
        except NotFoundError:
            return False
