from epic_events.models.role import Role
from epic_events.models.user import User
from epic_events.utils import has_permission
from epic_events.views.users_view import invalid_token
from epic_events.views.roles_views import (
    id_not_found, role_not_found, roles_table, created_succes)
from epic_events.views.users_view import logged_as

import rich_click as click
from sqlalchemy import select
import sentry_sdk


@click.group()
@click.pass_context
def role(ctx):
    """Allows only MANAGER, in reading mode."""
    pass


@role.command(name='list-role')
@click.option('--id', '-i', help='Name of the table to query', required=False)
@click.pass_context
@has_permission(['management'])
def list_role(ctx, id):
    session = ctx.obj['session']

    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        if id:
            role = session.scalar(select(Role).where(Role.id == id))
            if role is None:
                raise click.UsageError(role_not_found(id))
            else:
                roles_table([role])
        else:
            roles_list = session.scalars(
                select(Role).order_by(Role.id)).all()

            roles_table(roles_list)
            logged_as(user_logged.name, user_logged.role.name)

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)


@role.command()
@click.option('--name', '-n',
              help='Must be "support" "commercial" or "manager"',
              required=True)
@click.option('--id', '-i', help='Id to query', required=True)
@click.pass_context
@has_permission(['management'])
def create_role(ctx, name, id):
    session = ctx.obj['session']
    try:
        is_id = session.scalar(select(User).where(
            User.id == id)) if id is not None else None

        if Role.role_is_valid(ctx, None, name):
            if is_id is not None:
                new_role = Role(name=name)
                new_role.users.append(is_id)
                session.add(new_role)
                session.commit()
                created_succes(new_role)
            else:
                raise click.UsageError(id_not_found(id))

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)