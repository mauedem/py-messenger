import click
import inject
import uvicorn

from boot.containers import container
from interfaces.frontend_rpc.app import app


@click.group()
def start_cli():
    ...


@start_cli.command()
def start_rpc():
    inject.configure(container)
    uvicorn.run(app, host="127.0.0.1", port=5000)
