from litestar import Litestar

from .dependencies import db_connection
from .views.user import UserController

app = Litestar(route_handlers=[UserController], lifespan=[db_connection])
