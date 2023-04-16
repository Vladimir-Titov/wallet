from logging import getLogger
from typing import Callable

from fastapi_utils.errors import ClientError, AppError, ServerError
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = getLogger(__name__)


async def error_handler(request: Request, call_next: Callable):
    try:
        return await call_next(request)
    except BaseException as exc:
        log = logger.debug if isinstance(exc, ClientError) else logger.exception
        exc = exc if isinstance(exc, AppError) else ServerError(message='Unknown server error')
        log(exc)

        content = {
            'error': {
                'code': exc.code,
                'message': exc.message,
            }
        }

        if exc.errors is not None:
            content['error']['errors'] = exc.errors
        return JSONResponse(content, status_code=exc.status_code)
