from logging import getLogger
from typing import Optional, Union
from uuid import UUID

import arrow
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.asyncpg import PGDialect_asyncpg

logger = getLogger(__name__)
dialect = PGDialect_asyncpg(paramstyle='pyformat')


def compile_query(query):
    compiled = query.compile(dialect=dialect, compile_kwargs={"render_postcompile": True})
    compiled_params = sorted(compiled.params.items())
    mapping = {key: '$' + str(number) for number, (key, _) in enumerate(compiled_params, start=1)}
    new_query = compiled.string % mapping
    new_params = [val for key, val in compiled_params]
    logger.debug('\n%s', compiled.string % compiled.params)
    return new_query, new_params


def create(table: sa.Table, payload):
    return table.insert().values(payload).returning(table)


def count(table: sa.Table):
    return sa.select([sa.func.count()]).select_from(table)


def search(
    table: sa.Table,
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    query = table.select()
    if order_by:
        if order_by.startswith('-'):
            order_by_column = sa.desc(table.columns[order_by[1:]])
        else:
            order_by_column = table.columns[order_by]
        query = query.order_by(order_by_column)
    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query


def get_by_id(table: sa.Table, entity_id: Union[int, UUID]):
    return table.select().where(table.columns.id == entity_id)


def update(table: sa.Table, **kwargs):
    """Base query builder for update rows. Don't use it without filters!"""
    return table.update().values(updated=arrow.utcnow(), **kwargs).returning(table)


def update_by_id(table: sa.Table, entity_id: Union[int, UUID], **kwargs):
    return update(table, **kwargs).where(table.columns.id == entity_id)
