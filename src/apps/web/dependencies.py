import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar import Litestar
from litestar.datastructures import State

from core.user.repositories import UserRepository


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    from advanced_alchemy import config

    db = config.SQLAlchemyAsyncConfig(
        connection_string=os.environ["DB_DSN"],
        session_config=config.AsyncSessionConfig(expire_on_commit=False),
    )

    # TODO: миграции в файлах?
    from infra.db.models import UserModel

    async with db.get_engine().begin() as conn:
        await conn.run_sync(UserModel.metadata.create_all)

    async with db.get_session() as db_session:
        app.state.db_session = db_session
        yield


async def get_user_repository(state: State) -> UserRepository:
    from infra.db.repositories.user import DBUserRepository

    return DBUserRepository(db_session=state.db_session)
