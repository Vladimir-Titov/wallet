from app.repositories.accounts.repository import Accounts
from app.repositories.categories.repository import Categories
from app.repositories.clients.repository import Clients
from app.repositories.clients_categories.repository import ClientsCategories
from app.repositories.costs.repository import Costs
from app.repositories.currencies.repository import Currencies
from app.repositories.income.repository import Income


class WalletService:
    def __init__(
        self,
        accounts_repo: Accounts,
        clients_repo: Clients,
        categories_repo: Categories,
        clients_categories_repo: ClientsCategories,
        costs_repo: Costs,
        currencies_repo: Currencies,
        income_repo: Income,
    ):
        self.income_repo = income_repo
        self.currencies_repo = currencies_repo
        self.costs_repo = costs_repo
        self.clients_categories_repo = clients_categories_repo
        self.categories_repo = categories_repo
        self.accounts_repo = accounts_repo
        self.clients_repo = clients_repo
