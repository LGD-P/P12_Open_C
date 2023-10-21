import click
from epic_events.models.models import database
from epic_events.controllers.clients_controller import client
from epic_events.controllers.user_controller import user


@click.group()
@click.pass_context
@database
def app(ctx):
    pass


app.add_command(client)
app.add_command(user)
