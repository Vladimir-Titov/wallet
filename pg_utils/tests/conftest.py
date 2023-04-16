import pytest
from sqlalchemy import Boolean, Column, Table, String, TIMESTAMP, MetaData, text
from sqlalchemy.dialects.postgresql import UUID, JSONB

generate_uuid = text('uuid_generate_v4()')
now_at_utc = text("(now() at time zone 'utc')")


@pytest.fixture(scope='module')
def clients_table():
    return Table(
        'clients',
        MetaData(),
        Column('id', UUID, primary_key=True, server_default=generate_uuid),
        Column('first_name', String),
        Column('middle_name', String),
        Column('last_name', String),
        Column('email', String),
        Column('extra', JSONB),
        Column('created', TIMESTAMP, server_default=now_at_utc, nullable=False),
        Column('updated', TIMESTAMP, server_default=now_at_utc, nullable=False),
        Column('archived', Boolean, server_default='false', nullable=False),
    )


@pytest.fixture(scope='module')
def clients_log_table():
    return Table(
        'clients_log',
        MetaData(),
        Column('id', UUID),
        Column('first_name', String),
        Column('middle_name', String),
        Column('last_name', String),
        Column('email', String),
        Column('extra', JSONB),
        Column('created', TIMESTAMP),
        Column('updated', TIMESTAMP),
        Column('archived', Boolean),
    )
