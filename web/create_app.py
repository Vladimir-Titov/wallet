from logging import getLogger

from fastapi_pagination import add_pagination

from fastapi_utils import create_app
from fastapi_utils.initializers.clients.postgres import create_pg_pool
from settings import AppConfig, DbConfig
from .routes import routes

logger = getLogger(__name__)

app = create_app(routes, AppConfig.CORS)
create_pg_pool(app, DbConfig.CONNECTION_SETTINGS)
add_pagination(app)
