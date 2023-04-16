from random import randint
from uuid import uuid4

import pytest
import arrow
from sqlalchemy import insert, select, update, and_

from chili_pg_utils import query
from chili_pg_utils.tests.utils.utils import random_string


@pytest.mark.parametrize('payload', [
    {'id': uuid4()},
    {'id': uuid4(), 'first_name': random_string()},
    {'email': random_string()},
])
def test_create(clients_table, payload):
    actual = query.create(clients_table, payload)
    expected = insert(clients_table).values(**payload).returning(clients_table)
    assert expected.compare(actual)
    expected_str = (f"INSERT INTO clients ({', '.join(payload.keys())}) "
                    f"VALUES ({', '.join(f':{key}' for key in payload.keys())})")
    assert expected.compare(actual)
    assert expected_str in str(actual)


def test_count(clients_table):
    res = query.count(clients_table)
    expected = 'SELECT count(*) AS count_1 \nFROM clients'
    assert str(res) == expected


class TestSearch:

    def test_case1(self, clients_table):
        order_by, limit, offset = None, randint(1, 100), randint(1, 100)
        actual = query.search(clients_table, order_by=order_by, limit=limit, offset=offset)
        expected = clients_table.select().limit(limit).offset(offset)
        assert expected.compare(actual)
        assert str(actual) == str(expected)

    def test_case2(self, clients_table):
        order_by, limit, offset = 'created', randint(1, 100), randint(1, 100)
        actual = query.search(clients_table, order_by=order_by, limit=limit, offset=offset)
        expected = clients_table.select().order_by(
            clients_table.columns.created
        ).limit(limit).offset(offset)
        assert expected.compare(actual)
        assert str(actual) == str(expected)

    def test_case3(self, clients_table):
        order_by, limit, offset = '-created', randint(1, 100), randint(1, 100)
        actual = query.search(clients_table, order_by=order_by, limit=limit, offset=offset)
        expected = clients_table.select().order_by(
            clients_table.columns.created.desc()
        ).limit(limit).offset(offset)
        assert expected.compare(actual)
        assert str(actual) == str(expected)

    def test_case4(self, clients_table):
        order_by, limit, offset = None, None, 0
        actual = query.search(clients_table, order_by=order_by, limit=limit, offset=offset)
        expected = clients_table.select()
        assert expected.compare(actual)
        assert str(actual) == str(expected)


def test_get_by_id(clients_table):
    entity_id = uuid4()
    actual = query.get_by_id(clients_table, entity_id=entity_id)
    expected = select(clients_table).where(clients_table.columns.id == entity_id)
    assert expected.compare(actual)
    assert str(actual) == str(expected)


@pytest.mark.parametrize('payload', [
    {'id': uuid4()},
    {'id': uuid4(), 'first_name': random_string()},
    {'email': random_string()},
])
def test_update(clients_table, payload):
    actual = query.update(clients_table, **payload)
    expected = update(clients_table).values(
        dict(updated=arrow.utcnow(), **payload)
    ).returning(clients_table)
    assert str(actual) == str(expected)


@pytest.mark.parametrize('payload', [
    {'email': random_string(), 'first_name': random_string()},
    {'email': random_string()},
])
def test_update(clients_table, payload):
    entity_id = uuid4()
    actual = query.update_by_id(clients_table, entity_id=entity_id, **payload)
    expected = update(clients_table).values(
        dict(updated=arrow.utcnow(), **payload)
    ).where(clients_table.columns.id == entity_id).returning(clients_table)
    assert str(actual) == str(expected)


class TestCompileQuery:
    def test_select(self, clients_table):
        entity_id = uuid4()
        q = clients_table.select().where(and_(clients_table.c.id == entity_id))
        new_query, new_params = query.compile_query(q)
        expected_query = (f'SELECT {", ".join([f"clients.{col.name}" for col in clients_table.c])} '
                          f'\nFROM clients \nWHERE clients.id = $1')
        assert new_params == [entity_id]
        assert new_query == expected_query

    def test_update(self, clients_table):
        entity_id = uuid4()
        email = random_string()
        q = clients_table.update().values(email=email).where(and_(clients_table.c.id == entity_id))
        new_query, new_params = query.compile_query(q)
        expected_query = 'UPDATE clients SET email=$1 WHERE clients.id = $2'
        assert new_params == [email, entity_id]
        assert new_query == expected_query

    def test_create(self, clients_table):
        entity_id = uuid4()
        email = random_string()
        first_name = random_string()
        q = clients_table.insert().values(id=entity_id, email=email, first_name=first_name)
        new_query, new_params = query.compile_query(q)
        expected_query = 'INSERT INTO clients (id, first_name, email) VALUES ($3, $2, $1)'
        assert new_params == [email, first_name, entity_id]
        assert new_query == expected_query
