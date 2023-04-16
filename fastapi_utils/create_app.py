from typing import List, Tuple, Mapping, Callable

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from fastapi_utils.middleware import error_handler


def create_app(
    routes: List[Tuple],
    cors_settings: Mapping,
) -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    app.add_middleware(CORSMiddleware, **cors_settings)
    app.add_middleware(BaseHTTPMiddleware, dispatch=error_handler)
    for route in routes:
        route_path, route_description = route
        app.router.add_api_route(route_path, **route_description)

    return app
