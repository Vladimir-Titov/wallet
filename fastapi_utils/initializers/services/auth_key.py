from logging import getLogger

from aiohttp import ClientSession
from fastapi import FastAPI

logger = getLogger(__name__)

__all__ = ('get_auth_public_key',)


def get_auth_public_key(
    app: FastAPI,
    service_url: str,
    public_key_endpoint: str,
    auth_header_name: str,
    public_key_attribute: str,
):
    @app.on_event('startup')
    async def start():
        logger.debug('Try to get public key from %s', service_url)
        async with ClientSession(raise_for_status=True) as session:
            resp = await session.get(
                service_url + public_key_endpoint,
                headers={auth_header_name: f'Bearer {app.access_token}'}
            )
            resp = await resp.json()

        setattr(app, public_key_attribute, resp['data'])
        logger.debug(f'Public key stored in app.{public_key_attribute}')
