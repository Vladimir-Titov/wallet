from uuid import UUID

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .common import get_base_fields, meta, CommonModel

clients_categories = Table(
    'clients_categories',
    meta,
    *get_base_fields(),
    Column('client_id', PG_UUID, ForeignKey('clients.id')),
    Column('category_id', PG_UUID, ForeignKey('categories.id')),
)


class ClientCategory(CommonModel):
    client_id: UUID
    category_id: UUID
