from app.models import income
from pg_utils import EntityDBRepository


class Income(EntityDBRepository):
    entity = income
