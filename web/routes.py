from web.api import accounts, clients, categories

routes = [
    ('/accounts', accounts.create_account),
    ('/accounts', accounts.search_account),

    ('/clients', clients.create_client),
    ('/clients', clients.search_client),

    ('/categories', categories.create_category),
    ('/categories', categories.search_category),
]
