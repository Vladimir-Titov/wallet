from logging import getLogger

from asyncpg import Pool
from pg_utils import create_db_pool
from fastapi import FastAPI
from starlette.requests import Request

logger = getLogger(__name__)

__all__ = ('create_pg_pool', 'pg_pool')


def create_pg_pool(app: FastAPI, conn_settings):
    @app.on_event('startup')
    async def create():
        app.db_pool = await create_db_pool(**conn_settings)
        logger.debug('DB Connection is established')

        @app.on_event('shutdown')
        async def close():
            await app.db_pool.close()
            logger.debug('DB Connection is closed')


async def pg_pool(r: Request) -> Pool:
    return r.app.db_pool
