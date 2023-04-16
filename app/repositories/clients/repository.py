from app.models import clients
from pg_utils import EntityDBRepository


class Clients(EntityDBRepository):
    entity = clients
