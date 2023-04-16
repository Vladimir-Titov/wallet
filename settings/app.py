from .common import env


class AppConfig:
    PORT = env.int('PORT', 9000)
    HOST = env.str('HOST', '0.0.0.0')

    CORS = {
        'allow_origins': tuple(env.list('APP_ORIGIN_WHITELIST', default=['*'])),
        'allow_headers': tuple(env.list('APP_ALLOW_HEADERS', default=['*'])),
        'expose_headers': tuple(env.list('APP_EXPOSE_HEADERS', default=['*'])),
        'allow_credentials': env.bool('APP_ALLOW_CREDENTIALS', default=False),
        'max_age': env.int('APP_MAX_AGE', default=0),
    }
