import click
from epic_events.database import database
from epic_events.controllers.user_controller import user
from epic_events.controllers.clients_controller import client
from epic_events.controllers.contracts_controller import contract
from epic_events.controllers.events_controller import event
from epic_events.controllers.roles_controller import role
from epic_events.controllers.authenticate_controller import authenticate


@click.group()
@click.pass_context
@database
def app(ctx):
    pass


app.add_command(user)
app.add_command(client)
app.add_command(contract)
app.add_command(event)
app.add_command(role)
app.add_command(authenticate)
