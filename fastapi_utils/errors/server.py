from .base import AppError


class ServerError(AppError):
    status_code = 500


class GatewayTimeoutError(ServerError):
    status_code = 504


class ExternalError(ServerError):
    status_code = 500
