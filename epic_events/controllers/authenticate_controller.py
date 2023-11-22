from epic_events.models.user import User
from epic_events.views.users_view import (
    wrong_pass, username_not_found, login_success, logout_success, invalid_token)

from epic_events.utils import (
    generate_token, write_token_in_temp)


import click
from sqlalchemy import select
import os


@click.group()
@click.pass_context
def authenticate(ctx):
    """Manage user authentication, creating a token and logout deleting token"""
    pass


@authenticate.command()
@click.option('--name', '-n', help='Id of the user you want to delete',
              required=True)
@click.option('--password', '-P',
              help='Password of the user you want to login', nargs=0)
@click.pass_context
def login(ctx, name, password):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.name == name))
    if user:
        checking = User().confirm_pass(user.password)

        if not checking:
            wrong_pass()
            raise click.UsageError("Password does not match with user.")

        else:
            login_success(user.name)
            token = generate_token(user)
            write_token_in_temp(token)

    else:
        username_not_found(name)
        raise click.UsageError("User not found.")


@authenticate.command()
@click.pass_context
def logout(ctx):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        folder_path = 'temp'

        file_path_to_delete = os.path.join(folder_path, 'temporary.txt')

        for filename in os.listdir(folder_path):
            file_path_to_delete = os.path.join(folder_path, filename)
            os.unlink(file_path_to_delete)

        logout_success()

    except KeyError:
        invalid_token()