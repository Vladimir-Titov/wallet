from logging import getLogger

from aiohttp import ClientSession
from fastapi import FastAPI

logger = getLogger(__name__)

__all__ = ('create_http',)


def create_http(app: FastAPI, attr_name, **kwargs):
    @app.on_event('startup')
    async def create():
        session = ClientSession(**kwargs)
        setattr(app, attr_name, session)
        logger.debug(f'{attr_name} session is established')

        @app.on_event('shutdown')
        async def close():
            await session.close()
            logger.debug(f'{attr_name} session is closed')
