from datetime import datetime
from typing import TypeVar, List, Type

import arrow
from pydantic import BaseModel, create_model

T = TypeVar('T')
Y = TypeVar('Y')
DEFAULT_LIMIT = 100

scope = {}


class _Pagination(BaseModel):
    total: int
    limit: int = DEFAULT_LIMIT
    offset: int = 0


def paginated_response(model: Type):
    name = f'{model.__name__}PaginatedList'
    if name not in scope:
        scope[name] = create_model(
            name,
            items=(List[model], ...),
            pagination=(_Pagination, ...),
            __config__=model.Config,
        )
    return scope[name]


class ErrModel(BaseModel):
    code: str
    message: str
    errors: List[str]


class ErrRespModel(BaseModel):
    error: ErrModel


class ArrowField(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return arrow.get(v)
