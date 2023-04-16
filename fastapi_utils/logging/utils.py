import sys
from typing import List, Type

from aiohttp.web_log import AccessLogger
from .formatters import JSONFormatter


def create_logger_config(log_level: str, stand: str, loggers: dict):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            **loggers,
            '': {
                'level': log_level,
                'handlers': ['console'],
            },
            'root': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'generic' if stand == 'local' else 'json',
                'stream': sys.stdout,
            },
            'error_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'generic',
                'stream': sys.stderr,
            },
            'access_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'access',
                'stream': sys.stdout,
            },
        },
        'formatters': {
            'generic': {
                'format': '%(asctime)s (%(name)s)[%(levelname)s] %(message)s',
                'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
                'class': 'logging.Formatter',
            },
            'access': {
                'format': '%(asctime)s - (%(name)s)[%(levelname)s]: ' + '%(request)s %(message)s %(status)d %(byte)d',
                'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
                'class': 'logging.Formatter',
            },
            'json': {
                '()': JSONFormatter,
                'jsondumps_kwargs': {
                    'ensure_ascii': False,
                },
            },
        },
    }


def create_access_logger(non_logging_paths: List[str], access_log: bool) -> Type[AccessLogger]:
    class CustomAccessLogger(AccessLogger):

        def log(self, request, *args, **kwargs):
            if request.path in non_logging_paths:
                return
            if access_log:
                super().log(request, *args, **kwargs)

    return CustomAccessLogger
