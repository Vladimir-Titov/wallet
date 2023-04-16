from fastapi_utils.logging import create_logger_config
from .common import env

loggers = {
    'envparse': {
        'level': 'ERROR',
    },
}


class LogsConfig:
    LOG_LEVEL = env.str('LOG_LEVEL', default='DEBUG')
    UNLOG_PATH = ('/readiness', '/liveness')
    ACCESS_LOG = env.bool('LOGGING_ACCESS_LOG', default=True)
    LOGGING = create_logger_config(log_level=LOG_LEVEL, stand='local', loggers=loggers)
