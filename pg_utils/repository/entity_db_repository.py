from typing import Optional, Union, Mapping, List
from uuid import UUID

from sqlalchemy import Table

from pg_utils.errors import RowNotFoundError
from pg_utils.query import create, get_by_id, search, update_by_id, update, count
from pg_utils.types import PaginatedResponse, Pagination
from .db_repository import DBRepository


class EntityDBRepository(DBRepository):
	entity: Table
	entity_versions: Optional[Table] = None

	@property
	def has_version(self):
		return self.entity_versions is not None

	def _get_filter_bool_expression(self, filter_name, filter_value):
		if filter_name in self.entity.columns:
			return self.entity.columns[filter_name].__eq__(filter_value)

		split_by_underscore = filter_name.split('_')
		sign = split_by_underscore.pop()
		col_name = '_'.join(split_by_underscore)

		if sign in {'lt', 'le', 'gt', 'ge', 'ne'}:
			return getattr(self.entity.columns[col_name], f'__{sign}__')(filter_value)
		elif sign == 'in':
			return self.entity.columns[col_name].in_(filter_value)
		elif sign == 'notin':
			return ~self.entity.columns[col_name].in_(filter_value)
		elif sign == 'is':
			return self.entity.columns[col_name].is_(filter_value)
		elif sign == 'isnot':
			return self.entity.columns[col_name].is_not(filter_value)
		elif sign == 'like':
			return self.entity.columns[col_name].like(filter_value)
		elif sign == 'ilike':
			return self.entity.columns[col_name].ilike(filter_value)

		raise ValueError(f'Unknown filter name ({filter_name})')

	def _apply_filters(self, query, **filters):
		for filter_name, filter_value in filters.items():
			query = query.where(self._get_filter_bool_expression(filter_name, filter_value))

		return query

	async def count(self, **filters):
		query = count(self.entity)
		query = self._apply_filters(query, **filters)
		return await self.fetchval(query)

	async def create(self, **kwargs):
		payload = [kwargs]
		return await self.fetchrow(create(self.entity, payload))

	async def create_many(self, payload: List[Mapping]) -> List[dict]:
		return await self.fetch(create(self.entity, payload)) if payload else []

	async def search(
		self,
		order_by: Optional[str] = None,
		limit: Optional[int] = None,
		offset: int = 0,
		**filters,
	):
		query = search(self.entity, order_by=order_by, limit=limit, offset=offset)
		query = self._apply_filters(query, **filters)
		return await self.fetch(query)

	async def get_by_id(self, entity_id: Union[int, UUID]) -> dict:
		res = await self.fetchrow(get_by_id(table=self.entity, entity_id=entity_id))
		if not res:
			raise RowNotFoundError()
		return res

	async def get_or_create(self, **kwargs):
		existing_rows = await self.search(**kwargs)
		if len(existing_rows) == 1:
			return existing_rows[0]
		elif len(existing_rows) > 1:
			raise ValueError('Ambiguous value for %s' % kwargs)

		return await self.create(**kwargs)

	async def update_by_id(self, entity_id: Union[int, UUID], **payload) -> dict:
		update_query = update_by_id(table=self.entity, entity_id=entity_id, **payload)
		res = await self.fetchrow(update_query)
		if not res:
			raise RowNotFoundError("No row has been updated")
		return res

	async def update(self, payload: Mapping, **filters) -> List:
		update_query = update(self.entity, **payload)
		update_query = self._apply_filters(update_query, **filters)

		return await self.fetch(update_query)

	async def archive_by_id(self, entity_id: Union[int, UUID]) -> dict:
		return await self.update_by_id(entity_id=entity_id, archived=True)

	async def archive(self, **filters) -> List:
		return await self.update({'archived': True}, **filters)

	async def paginated_search(
		self,
		order_by: Optional[str] = None,
		limit: Optional[int] = None,
		offset: int = 0,
		**filters,
	):
		items = await self.search(order_by, limit, offset, **filters)
		total = await self.count(**filters)

		return PaginatedResponse(
			items=items,
			pagination=Pagination(
				limit=limit,
				offset=offset,
				total=total,
			),
		)
