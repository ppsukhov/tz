import datetime
from typing import Self

from litestar import Controller, Response, delete, get, patch, post
from litestar.di import Provide
from pydantic import BaseModel, model_validator

from apps.web.dependencies import get_user_repository
from core.shared.utils import create_password_hash
from core.user.repositories import UserRepository


class CreateUserRequestModel(BaseModel):
    name: str
    surname: str
    password: str


class UpdateUserRequestModel(BaseModel):
    name: str | None = None
    surname: str | None = None

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.name is None and self.surname is None:
            raise ValueError("Empty data")
        return self


class UserResponseModel(BaseModel):
    id: int
    name: str
    surname: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserController(Controller):
    path = "/users"
    dependencies = {"user_repository": Provide(get_user_repository, use_cache=True)}

    @post(path="")
    async def create_user(
        self,
        data: CreateUserRequestModel,
        user_repository: UserRepository,
    ) -> UserResponseModel:
        item = await user_repository.create(
            data.model_dump() | {"password": create_password_hash(data.password)}
        )
        return UserResponseModel.model_construct(**item.model_dump())

    @get(path="")
    async def get_users_list(
        self,
        user_repository: UserRepository,
    ) -> list[UserResponseModel]:
        return [
            UserResponseModel.model_construct(**i.model_dump())
            for i in await user_repository.get_all()
        ]

    @get(path="/{user_id:int}")
    async def get_user(
        self,
        user_id: int,
        user_repository: UserRepository,
    ) -> UserResponseModel | Response:
        item = await user_repository.find_by_id(item_id=user_id)
        if not item:
            return Response(status_code=404, content=None)

        return UserResponseModel.model_construct(**item.model_dump())

    @patch(path="/{user_id:int}")
    async def update_user(
        self,
        user_id: int,
        data: UpdateUserRequestModel,
        user_repository: UserRepository,
    ) -> UserResponseModel:
        item = await user_repository.update(user_id, data.model_dump(exclude_none=True))
        if not item:
            return Response(status_code=404, content=None)

        return UserResponseModel.model_construct(**item.model_dump())

    @delete(path="/{user_id:int}")
    async def delete_user(
        self,
        user_id: int,
        user_repository: UserRepository,
    ) -> None:
        if not await user_repository.delete_by_id(item_id=user_id):
            return Response(status_code=404, content=None)
