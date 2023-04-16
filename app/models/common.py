from typing import Optional
from uuid import UUID

import arrow
from pydantic import BaseModel, PositiveInt, NonNegativeInt
from sqlalchemy import MetaData, Column, Boolean, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy_utils import ArrowType

from fastapi_utils.types import ArrowField
from settings import DbConfig

meta = MetaData('web_wallet')
now_at_utc = text("(now() at time zone 'utc')")
generate_uuid = text('uuid_generate_v4()')

base_fields = ['id', 'created', 'updated', 'archived']


def get_base_fields():
    return (
        Column('id', PG_UUID, primary_key=True, server_default=generate_uuid, nullable=False),
        Column('created', ArrowType, server_default=now_at_utc, nullable=False),
        Column('updated', ArrowType, server_default=now_at_utc, nullable=False),
        Column('archived', Boolean, server_default='false'),
    )


class CommonModel(BaseModel):
    id: UUID
    created: ArrowField
    updated: ArrowField
    archived: bool

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
        orm_mode = True


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
        orm_mode = True


class BaseFilters(BaseModel):
    limit: PositiveInt = DbConfig.DEFAULT_LIMIT
    offset: NonNegativeInt = 0

    archived: Optional[bool] = False
