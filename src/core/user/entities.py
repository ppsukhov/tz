import datetime
from typing import ClassVar, NewType

from core.shared.entities import Entity


class User(Entity):
    ID: ClassVar = NewType("User.ID", int)

    id: ID
    name: str
    surname: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
