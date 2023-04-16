from app.models import clients_categories
from pg_utils import EntityDBRepository


class ClientsCategories(EntityDBRepository):
    entity = clients_categories
