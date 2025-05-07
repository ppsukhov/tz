from advanced_alchemy.extensions.litestar import (
    base,
)
from sqlalchemy.orm import Mapped


class UserModel(base.BigIntAuditBase):
    __tablename__ = "user"

    name: Mapped[str]
    surname: Mapped[str]
    password: Mapped[str]
