from app.models import costs
from pg_utils import EntityDBRepository


class Costs(EntityDBRepository):
    entity = costs
