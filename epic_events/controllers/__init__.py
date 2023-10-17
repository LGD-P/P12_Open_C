import click
from epic_events.models.models import database
from epic_events.controllers.clients_controller import client


@click.group()
@click.pass_context
@database
def app(ctx):
    pass


app.add_command(client)
