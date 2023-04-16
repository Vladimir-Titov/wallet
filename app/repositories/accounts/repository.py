from app.models.account import accounts
from pg_utils import EntityDBRepository


class Accounts(EntityDBRepository):
    entity = accounts
