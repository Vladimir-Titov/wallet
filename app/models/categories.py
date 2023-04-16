from sqlalchemy import Table, Column, String

from .common import get_base_fields, meta, CommonModel

categories = Table(
    'categories',
    meta,
    *get_base_fields(),
    Column('label', String),
)


class Category(CommonModel):
    label: str
