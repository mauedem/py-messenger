import click
import inject

from boot.containers import container
from interfaces.frontend_rpc.app import app


@click.group()
def start_cli():
        ...


@start_cli.command()
def start_rpc():
        inject.configure(container)
        app.run()


