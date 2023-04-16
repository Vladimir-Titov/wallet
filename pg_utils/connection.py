from datetime import timedelta
from logging import getLogger

import arrow
from asyncpg import Connection, Pool, create_pool
from ujson import dumps, loads

from .types import Interval

logger = getLogger(__name__)

TIMESTAMP_2000Y = arrow.get('2000-01-01').float_timestamp
DATETIME_2000Y = arrow.get('2000-01-01').datetime


def create_db_pool(dsn, **kwargs) -> Pool:
    return create_pool(dsn=dsn, init=_init_connection, **kwargs)


async def _init_connection(con: Connection):
    def _encoder(value):
        return b'\x01' + dumps(value).encode('utf-8')

    def _decoder(value):
        return loads(value[1:].decode('utf-8'))

    await con.set_type_codec(
        'jsonb',
        encoder=_encoder,
        decoder=_decoder,
        schema='pg_catalog',
        format='binary',
    )

    await con.set_type_codec(
        'timestamp',
        encoder=lambda x: int.to_bytes(
            int((x.float_timestamp - TIMESTAMP_2000Y) * 1000000), byteorder='big', length=8,
        ),
        decoder=lambda x: arrow.get(DATETIME_2000Y + timedelta(
            microseconds=int.from_bytes(x, byteorder='big'),
        )),
        schema='pg_catalog',
        format='binary',
    )

    await con.set_type_codec(
        'timestamptz',
        encoder=lambda x: int.to_bytes(
            int((x.float_timestamp - TIMESTAMP_2000Y) * 1000000), byteorder='big', length=8,
        ),
        decoder=lambda x: arrow.get(DATETIME_2000Y + timedelta(
            microseconds=int.from_bytes(x, byteorder='big'),
        )),
        schema='pg_catalog',
        format='binary',
    )

    await con.set_type_codec(
        'interval',
        encoder=lambda x: (
            x.years * 12 + x.months,
            x.days,
            (x.hours * 3600 + x.minutes * 60 + x.seconds) * 1000000 + x.microseconds,
        ),
        decoder=lambda x: Interval(
            years=x[0] // 12,
            months=x[0] % 12,
            days=x[1],
            hours=x[2] // 1000000 // 60 // 60,
            minutes=x[2] // 1000000 // 60 % 60,
            seconds=(x[2] // 1000000) % 60,
            microseconds=x[2] % 1000000,
        ),
        schema='pg_catalog',
        format='tuple',
    )
