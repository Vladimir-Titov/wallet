from app.models import currencies
from pg_utils import EntityDBRepository


class Currencies(EntityDBRepository):
    entity = currencies
