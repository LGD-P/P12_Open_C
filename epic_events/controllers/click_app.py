import rich_click as click
from epic_events.database import create_database
from epic_events.controllers.user_controller import user
from epic_events.controllers.clients_controller import client
from epic_events.controllers.contracts_controller import contract
from epic_events.controllers.events_controller import event
from epic_events.controllers.roles_controller import role
from epic_events.controllers.authenticate_controller import authenticate
from epic_events.utils import check_token_to_get_user
from epic_events.views.users_view import invalid_token

click.rich_click.COMMAND_GROUPS = {
    "cli": [
        {
            "commands": ["generate-password", "passphrase", "test-pass"],
            "table_styles": {
                "show_lines": True,
                "row_styles": ["magenta", "yellow", "cyan", "green"],
                "border_style": "red",
                "box": "DOUBLE",
            },
        },
    ],
}


@click.group()
@click.pass_context
def app(ctx):
    ctx.ensure_object(dict)
    db_session = create_database()
    user_id = check_token_to_get_user(db_session)
    ctx.obj['session'] = db_session
    if user_id:
        ctx.obj['user_id'] = user_id


app.add_command(user)
app.add_command(client)
app.add_command(contract)
app.add_command(event)
app.add_command(role)
app.add_command(authenticate)
