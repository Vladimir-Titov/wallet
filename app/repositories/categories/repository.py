from app.models import categories
from pg_utils import EntityDBRepository


class Categories(EntityDBRepository):
    entity = categories
