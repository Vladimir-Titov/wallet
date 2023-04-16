from random import randint
from unittest.mock import Mock, AsyncMock, MagicMock
from uuid import uuid4

import pytest
import sqlalchemy as sa

from chili_pg_utils.query import search, update, create, get_by_id, update_by_id, count
from chili_pg_utils.repository.entity_db_repository import EntityDBRepository
from chili_pg_utils.tests.utils.utils import random_string, proxy_args
from chili_pg_utils.types import PaginatedResponse, Pagination

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mocked_entity_db_repo(clients_table, clients_log_table):
    mocked_repo = EntityDBRepository(db_pool=Mock())
    mocked_repo.fetch = AsyncMock(side_effect=proxy_args)
    mocked_repo.fetchrow = AsyncMock(side_effect=proxy_args)
    mocked_repo.fetchval = AsyncMock(side_effect=proxy_args)
    mocked_repo.connection = MagicMock()
    mocked_repo.transaction = MagicMock()
    return mocked_repo


@pytest.fixture
def clients_repo(mocked_entity_db_repo, clients_table):
    mocked_entity_db_repo.entity = clients_table
    return mocked_entity_db_repo


@pytest.fixture
def clients_repo_with_versions(mocked_entity_db_repo, clients_table, clients_log_table):
    mocked_entity_db_repo.entity = clients_table
    mocked_entity_db_repo.entity_versions = clients_log_table
    return mocked_entity_db_repo


@pytest.mark.parametrize('filters', [
    {},
    {'id': uuid4()},
    {'id': uuid4(), 'first_name': random_string()},
    {'email': 'test@test.id'},
])
async def test_apply_filters(clients_repo, filters):
    res = clients_repo._apply_filters(clients_repo.entity.select(), **filters)
    if not filters:
        assert res.whereclause is None
    else:
        query = sa.select(clients_repo.entity)
        for k, v in filters.items():
            query = query.where(clients_repo.entity.columns[k] == v)
        assert query.compare(res)


class TestGetFilterBoolExpression:

    async def test_positive(self, clients_repo, clients_table):
        rand_value = random_string()

        res = clients_repo._get_filter_bool_expression('created', rand_value)
        assert res.compare(clients_table.columns.created == rand_value)

        res = clients_repo._get_filter_bool_expression('created_lt', rand_value)
        assert res.compare(clients_table.columns.created < rand_value)

        res = clients_repo._get_filter_bool_expression('created_le', rand_value)
        assert res.compare(clients_table.columns.created <= rand_value)

        res = clients_repo._get_filter_bool_expression('created_gt', rand_value)
        assert res.compare(clients_table.columns.created > rand_value)

        res = clients_repo._get_filter_bool_expression('created_ge', rand_value)
        assert res.compare(clients_table.columns.created >= rand_value)

        res = clients_repo._get_filter_bool_expression('created_ne', rand_value)
        assert res.compare(clients_table.columns.created != rand_value)

        res = clients_repo._get_filter_bool_expression('created_in', [rand_value])
        assert res.compare(clients_table.columns.created.in_([rand_value]))

        res = clients_repo._get_filter_bool_expression('created_notin', [rand_value])
        assert res.compare(~clients_table.columns.created.in_([rand_value]))

        res = clients_repo._get_filter_bool_expression('created_like', rand_value)
        assert res.compare(clients_table.columns.created.like(rand_value))

        res = clients_repo._get_filter_bool_expression('created_ilike', rand_value)
        assert res.compare(clients_table.columns.created.ilike(rand_value))

        res = clients_repo._get_filter_bool_expression('archived_is', True)
        assert res.compare(clients_table.columns.archived.is_(True))

        res = clients_repo._get_filter_bool_expression('archived_isnot', False)
        assert res.compare(clients_table.columns.archived.is_not(False))

    async def test_negative(self, clients_repo, clients_table):
        with pytest.raises(ValueError):
            clients_repo._get_filter_bool_expression('created_sadlfsdjf', random_string())


@pytest.mark.parametrize('order_by, limit, offset, filters', [
    (None, None, 0, {}),
    ('created', 100, 20, {}),
    ('-created', None, 0, {}),
    (None, None, 0, {'id': 'test_id'}),
])
async def test_search(clients_repo, order_by, limit, offset, filters):
    fetched_args, _fetched_kwargs = await clients_repo.search(
        order_by=order_by,
        limit=limit,
        offset=offset,
        **filters
    )
    expected_query = search(clients_repo.entity, order_by=order_by, limit=limit, offset=offset)
    expected_query = clients_repo._apply_filters(expected_query, **filters)
    assert expected_query.compare(fetched_args[0])


@pytest.mark.parametrize('filters', [
    {},
    {'email': 'test@test.id'},
    {'id': uuid4(), 'email': 'test@test.id'},
    {'first_name': random_string()},
])
async def test_count(clients_repo, filters):
    fetched_args, _fetched_kwargs = await clients_repo.count(**filters)
    expected_query = count(clients_repo.entity)
    expected_query = clients_repo._apply_filters(expected_query, **filters)
    assert expected_query.compare(fetched_args[0])


class TestCreate:
    async def test_with_args(self, clients_repo):
        fetched_args, _fetched_kwargs = await clients_repo.create(1, 2, 3)
        expected_query = create(clients_repo.entity, [1, 2, 3])
        assert expected_query.compare(fetched_args[0])

    async def test_with_kwargs(self, clients_repo):
        kwargs = {'id': '123', 'email': 'test@test.id'}
        fetched_args, _fetched_kwargs = await clients_repo.create(**kwargs)
        expected_query = create(clients_repo.entity, [kwargs])
        assert expected_query.compare(fetched_args[0])


async def test_create_many(clients_repo):
    create_payload = [
        {random_string(): random_string()},
        {random_string(): random_string()},
    ]
    fetched_args, _fetched_kwargs = await clients_repo.create_many(create_payload)
    expected_query = create(clients_repo.entity, create_payload)
    assert expected_query.compare(fetched_args[0])


async def test_get_by_id(clients_repo):
    fetched_args, _fetched_kwargs = await clients_repo.get_by_id(1)
    expected_query = get_by_id(table=clients_repo.entity, entity_id=1)
    assert expected_query.compare(fetched_args[0])


async def test_get_or_create(clients_repo):
    expected = random_string()
    clients_repo.fetch.side_effect = [[expected], [random_string(), random_string()]]
    actual = await clients_repo.get_or_create()
    assert expected == actual

    try:
        await clients_repo.get_or_create()
    except ValueError:
        pass


class TestUpdateById:

    @pytest.fixture(autouse=True)
    def init(self, clients_table, clients_log_table):
        self.entity_id = uuid4()
        self.payload = {'email': random_string(), 'archived': True}
        self.expected_query = update_by_id(
            table=clients_table, entity_id=self.entity_id, **self.payload
        )

    async def test_base(self, clients_repo):
        clients_repo._update = AsyncMock(side_effect=proxy_args)
        update_args, _update_kwargs = await clients_repo.update_by_id(
            self.entity_id, **self.payload
        )
        assert str(self.expected_query) == str(update_args[0])


class TestUpdate:

    async def test_base(self, clients_repo):
        clients_repo._update = AsyncMock(side_effect=proxy_args)
        payload = {'archived': True, 'email': random_string()}
        filters = {'id': 123}
        update_args, _update_kwargs = await clients_repo.update(
            payload, **filters
        )
        expected_query = update(clients_repo.entity, **payload)
        expected_query = clients_repo._apply_filters(expected_query, **filters)
        assert str(expected_query) == str(update_args[0])


async def test_archived_by_id(clients_repo):
    entity_id = uuid4()
    clients_repo.update_by_id = AsyncMock(side_effect=proxy_args)
    _update_args, update_kwargs = await clients_repo.archive_by_id(entity_id)
    expected_kwargs = {'entity_id': entity_id, 'archived': True}
    assert expected_kwargs == update_kwargs


@pytest.mark.parametrize('filters', [
    {'id': 123}, {'id': uuid4(), 'first_name': random_string()}, {'email': random_string()}
])
async def test_archived(clients_repo, filters):
    clients_repo.update = AsyncMock(side_effect=proxy_args)
    update_args, update_kwargs = await clients_repo.archive(**filters)
    expected_kwargs = filters
    expected_args = {'archived': True}
    assert expected_args == update_args[0]
    assert expected_kwargs == update_kwargs


@pytest.mark.parametrize('search_res, count_res, order_by, limit, offset, filters', [
    ([{'id': uuid4()}], 1, 'created', randint(1, 100), randint(1, 100), {'first_name': random_string()}),
    ([{'id': uuid4()}, {'first_name': random_string()}], 2, 'updated', randint(1, 100), randint(1, 100), {})
])
async def test_paginated_response(
    clients_repo,
    search_res,
    count_res,
    order_by,
    limit,
    offset,
    filters,
):
    clients_repo.search = AsyncMock()
    clients_repo.search.return_value = search_res
    clients_repo.count = AsyncMock()
    clients_repo.count.return_value = count_res

    actual = await clients_repo.paginated_search(
        order_by=order_by,
        limit=limit,
        offset=offset,
        **filters
    )
    expected = PaginatedResponse(
        items=search_res,
        pagination=Pagination(
            limit=limit,
            offset=offset,
            total=count_res,
        ),
    )

    assert clients_repo.search.await_args.args == (order_by, limit, offset)
    assert clients_repo.search.await_args.kwargs == filters
    assert clients_repo.count.await_args.kwargs == filters
    assert actual == expected
