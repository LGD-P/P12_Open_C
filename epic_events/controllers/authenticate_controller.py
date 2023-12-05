from epic_events.models.user import User
from epic_events.views.users_view import (
    wrong_pass, login_success, logout_success, invalid_token, user_email_not_found)
from epic_events.utils import (
    generate_token, write_token_in_temp)

import rich_click as click
from sqlalchemy import select
import os
import sentry_sdk


@click.group()
@click.pass_context
def authenticate(ctx):
    """Manage user authentication, creating a token and logout deleting token"""
    pass


@authenticate.command()
@click.option('--email', '-e', help='Email of user that you want to login ',
              required=True)
@click.option('--password', '-P',
              help='Password of the user you want to login', nargs=0)
@click.pass_context
def login(ctx, email, password):
    """Login : -e + 'email', your password will automatically be asked"""
    session = ctx.obj['session']
    try:
        user = session.scalar(select(User).where(User.email == email))
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
            error = user_email_not_found(email)
            raise Exception('User not in DB', error)

    except Exception as e:
        sentry_sdk.capture_exception(e)


@authenticate.command()
@click.pass_context
def logout(ctx):
    """Logout : You juste have to 'logout'"""
    session = ctx.obj['session']
    try:
        session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        folder_path = 'temp'

        file_path_to_delete = os.path.join(folder_path, 'temporary.txt')

        for filename in os.listdir(folder_path):
            file_path_to_delete = os.path.join(folder_path, filename)
            os.unlink(file_path_to_delete)

        logout_success()

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception("invalid token", message)
