from .common import env


class DbConfig:
    DB_URL = env.str('DB_URL', default='postgresql://postgres:postgres@postgres:5432')
    DEFAULT_LIMIT = env.int('DEFAULT_LIMIT', 100)
    CONNECTION_SETTINGS = {
        'dsn': env.str('DB_URL', default='postgresql://postgres:postgres@0.0.0.0:54329/postgres'),
        'min_size': env.int('DB_POOL_MIN_SIZE', default=1),
        'max_size': env.int('DB_POOL_MAX_SIZE', default=2),
        'max_inactive_connection_lifetime': env.float('DB_POOL_MAX_INACTIVE_CONNECTION_LIFETIME', default=300),
        'timeout': env.int('DB_TIMEOUT', default=60),
        'statement_cache_size': env.int('DB_STATEMENT_CACHE_SIZE', default=1024),
    }
