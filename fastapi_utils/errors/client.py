from .base import AppError


class ClientError(AppError):
    status_code = 400


class NotFoundError(ClientError):
    status_code = 404


class ForbiddenError(ClientError):
    status_code = 403


class UnauthorizedError(ClientError):
    status_code = 401


class ValidationError(ClientError):
    status_code = 400


class BadTokenError(UnauthorizedError):
    pass
