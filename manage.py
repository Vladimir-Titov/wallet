import platform
from logging import config as logging_config

import click as click
import uvicorn

from settings import AppConfig, LogsConfig
from web import app


@click.group()
def cli():
    logging_config.dictConfig(LogsConfig.LOGGING)
    if platform.system() != 'Windows':
        import uvloop  # noqa: WPS433 - will fail on Windows
        uvloop.install()


@cli.command(short_help='start')
def start():
    uvicorn.run(app, host=AppConfig.HOST, port=AppConfig.PORT)


if __name__ == '__main__':
    cli()
