import contextvars
from contextlib import asynccontextmanager

from asyncpg import Connection, Pool

from pg_utils.query import compile_query

db_ctx = contextvars.ContextVar('connection')


class DBRepository:
    def __init__(self, db_pool: Pool):
        db_ctx.set(db_pool)
        self.db_pool = db_pool

    @asynccontextmanager
    async def connection(self):
        con = db_ctx.get()
        if isinstance(con, Connection):
            yield con

        if isinstance(con, Pool):
            async with con.acquire() as conn:
                db_ctx.set(conn)
                try:
                    yield conn
                finally:
                    db_ctx.set(self.db_pool)

    @asynccontextmanager
    async def transaction(self):
        async with self.connection() as con:
            async with con.transaction():
                yield con

    async def fetch(self, query):
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            records = await con.fetch(compiled_query, *compiled_params)
            return [dict(record) for record in records]

    async def fetchrow(self, query):
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            record = await con.fetchrow(compiled_query, *compiled_params)
            return dict(record) if record else None

    async def fetchval(self, query):
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            return await con.fetchval(compiled_query, *compiled_params)
