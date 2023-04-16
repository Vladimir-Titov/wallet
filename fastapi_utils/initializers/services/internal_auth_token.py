import asyncio
from logging import getLogger

from aiohttp import ClientSession
from fastapi import FastAPI
from starlette.requests import Request

logger = getLogger(__name__)

__all__ = ('get_app_access_token', 'auth_access_token')


async def refresh_token(app: FastAPI, url):
    logger.debug('Start session refreshing')
    resp = await app.auth_session.post(
        url + '/refresh_session',
        json={'access_token': app.access_token, 'refresh_token': app.refresh_token},
    )
    tokens = await resp.json()
    app.access_token = tokens['data']['access_token']
    app.refresh_token = tokens['data']['refresh_token']
    logger.debug('Session is refreshed, access key is updated')


async def token_refresh_task(app, url, refresh_token_timeout):
    while True:
        await asyncio.sleep(refresh_token_timeout)
        await refresh_token(app, url)


def get_app_access_token(
    app: FastAPI,
    url: str,
    username: str,
    password: str,
    refresh_token_timeout: int,
):
    @app.on_event('startup')
    async def start():
        app.auth_session = ClientSession(raise_for_status=True)
        resp = await app.auth_session.post(
            url + '/login_by_username',
            json={'mail': username, 'password': password},
        )
        tokens = await resp.json()
        app.access_token = tokens['data']['access_token']
        app.refresh_token = tokens['data']['refresh_token']
        app.auth_task = asyncio.create_task(token_refresh_task(app, url, refresh_token_timeout))

        @app.on_event('shutdown')
        async def close():
            await app.auth_session.close()
            app.auth_task.cancel()
            logger.debug('auth session is closed, refresh tasks is cancelled')


async def auth_access_token(r: Request) -> str:
    return r.app.auth_access_token
