from typing import Optional

from sqlalchemy import Table, Column, String

from .common import get_base_fields, meta, CommonModel

clients = Table(
    'clients',
    meta,
    *get_base_fields(),
    Column('email', String),
    Column('first_name', String),
    Column('last_name', String),
)


class Client(CommonModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
