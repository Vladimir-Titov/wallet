from fastapi import Depends
from sqlalchemy.pool import Pool

from app.repositories.accounts.repository import Accounts
from app.repositories.categories.repository import Categories
from app.repositories.clients.repository import Clients
from app.repositories.clients_categories.repository import ClientsCategories
from app.repositories.costs.repository import Costs
from app.repositories.currencies.repository import Currencies
from app.repositories.income.repository import Income
from app.services.wallet import WalletService
from fastapi_utils.initializers.clients.postgres import pg_pool


async def wallet_service(db_pool: Pool = Depends(pg_pool)) -> WalletService:
    return WalletService(
        accounts_repo=Accounts(db_pool=db_pool),
        clients_repo=Clients(db_pool=db_pool),
        categories_repo=Categories(db_pool=db_pool),
        clients_categories_repo=ClientsCategories(db_pool=db_pool),
        currencies_repo=Currencies(db_pool=db_pool),
        costs_repo=Costs(db_pool=db_pool),
        income_repo=Income(db_pool=db_pool),
    )
