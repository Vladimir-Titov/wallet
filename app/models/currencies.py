from sqlalchemy import Table, Column, String

from .common import get_base_fields, meta, CommonModel

currencies = Table(
    'currencies',
    meta,
    *get_base_fields(),
    Column('label', String),
)


class Currency(CommonModel):
    label: str
