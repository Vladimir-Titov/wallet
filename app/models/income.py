from typing import Optional
from uuid import UUID

from sqlalchemy import Table, Column, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .common import get_base_fields, meta, CommonModel

income = Table(
    'income',
    meta,
    *get_base_fields(),
    Column('category_id', PG_UUID, ForeignKey('categories.id')),
    Column('account_id', PG_UUID, ForeignKey('accounts.id')),
    Column('amount', Numeric(precision=12, scale=2)),
    Column('comment', String),
)


class Income(CommonModel):
    category_id: UUID
    account_id: UUID
    amount: float
    comment: Optional[str] = None
