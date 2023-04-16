from typing import Optional
from uuid import UUID

from sqlalchemy import Table, Column, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .common import get_base_fields, meta, CommonModel

accounts = Table(
    'accounts',
    meta,
    *get_base_fields(),
    Column('currency_id', PG_UUID, ForeignKey('currencies.id')),
    Column('client_id', PG_UUID, ForeignKey('clients.id')),
    Column('label', String),
    Column('balance', Numeric(precision=12, scale=2)),
)


class Account(CommonModel):
    currency_id: UUID
    client_id: UUID
    label: str
    balance: Optional[float] = 0.0
