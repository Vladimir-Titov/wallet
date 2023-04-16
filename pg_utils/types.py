from dataclasses import dataclass
from typing import List, Mapping


@dataclass
class Pagination:
    limit: int
    offset: int
    total: int


@dataclass
class PaginatedResponse:
    items: List[Mapping]
    pagination: Pagination


@dataclass
class Interval:
    days: int = 0
    months: int = 0
    years: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    microseconds: int = 0
