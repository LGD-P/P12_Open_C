from epic_events.models.user import User
from epic_events.models.role import Role
from epic_events.utils import has_permission
from epic_events.views.users_view import (invalid_token, logged_as,
                                          users_table, created_succes,
                                          deleted_success, user_not_found,
                                          modification_done, wrong_pass,
                                          new_pass, invalid_pass,
                                          invalid_email)

import rich_click as click
from sqlalchemy import select
import re


@click.group()
@click.pass_context
def user(ctx):
    """Allows only MANAGER, within the limits of their permissions, to access various operations of the User CRUD."""
    pass


def email_is_valid(ctx, param, value):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, value):
        return value
    else:
        invalid_email()
        raise click.UsageError("Invalid email.")


def pass_is_valid(ctx, param, value):
    regex = re.compile(
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
    if value != ctx.params.get('password', None) \
            and re.fullmatch(regex, value) is None:
        invalid_pass()
        raise click.UsageError(
            "Invalid password. Passwords do not match or not strong enough.")
    return value


def change_password(user_to_modify, ctx):
    checking = User().confirm_pass(user_to_modify.password)

    if not checking:
        wrong_pass()
        raise click.UsageError("Password does not match with user.")

    new_password = new_pass()
    pass_is_valid(ctx, param=None, value=new_password)

    new_password = User().hash_pass(new_password)

    confirmed = User().confirm_pass(new_password)

    if not confirmed:
        wrong_pass()
        raise click.UsageError("You confirmed a wrong password.")

    return new_password


@user.command()
@click.option('--id', '-i', help='Id of the user to query')
@click.pass_context
@has_permission(['management'])
def list_user(ctx, id):
    session = ctx.obj['session']

    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        if id:
            user = session.scalar(select(User).where(User.id == id))

            if user is None:
                user_not_found(id)
            else:
                users_table([user])
        else:
            users_list = session.scalars(
                select(User).order_by(User.id)).all()

            users_table(users_list)
            logged_as(user_logged.name, user_logged.role.name)

    except KeyError:
        invalid_token()
        pass


@user.command()
@click.option('--name', '-n', help='Name for the new object', required=True)
@click.option('--email', '-e', help='Email for the new object', required=True,
              callback=email_is_valid)
@click.option('--role', '-r',
              help='Role must be : support management or commercial',
              required=True, callback=Role.role_is_valid)
@click.option('--password', '-P',
              help='Password will automaticly be asked don\'t use this option',
              prompt=True, hide_input=True,
              # confirmation_prompt=True,
              default=None, callback=pass_is_valid)
@click.pass_context
@has_permission(['management'])
def create_user(ctx, name, email, role, password):
    session = ctx.obj['session']
    try:
        session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        role_to_fill = session.scalars(
            select(Role).where(Role.name == role)).one()

        hashed_password = User().hash_pass(password)

        new_user = User(name=name, email=email,
                        role=role_to_fill, password=hashed_password)

        session.add(new_user)
        session.commit()

        role_to_fill.users.append(new_user)
        session.add(role_to_fill)
        session.commit()

        created_succes(new_user)
    except KeyError:
        invalid_token()


@user.command()
@click.option('--id', '-i', help='Id of the user you want to modify',
              required=True)
@click.option('--name', '-n', help='New name of the user')
@click.option('--email', '-e', help='New email of the user')
@click.option('--role', '-r', help='New role of the user, must be: '
                                   'support management or commercial')
@click.option('--password', '-P', help='-P without argument', nargs=0)
@click.pass_context
@has_permission(['management'])
def modify_user(ctx, id, name, email, role, password):
    session = ctx.obj['session']
    try:
        session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        user_to_modify = session.scalar(select(User).where(User.id == id))
        if user_to_modify:

            if name is not None:
                user_to_modify.name = name

            if email is not None:
                email = email_is_valid(ctx, None, email)
                user_to_modify.email = email

            if role is not None:
                role = Role().role_is_valid(ctx, role)
                role_to_give = session.scalar(select(Role).where(
                    Role.name == role))
                user_to_modify.role_id = role_to_give.id

            if password is not None:
                new_password = change_password(user_to_modify, ctx)
                user_to_modify.password = new_password

            session.commit()
            modification_done(user_to_modify)
        else:
            user_not_found(id)
    except KeyError:
        invalid_token()


@user.command()
@click.option('--id', '-i', help='Id of the user you want to delete',
              required=True)
@click.pass_context
@has_permission(['management'])
def delete_user(ctx, id):
    session = ctx.obj['session']
    try:
        session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        user_to_delete = session.scalar(select(User).where(User.id == id))

        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            deleted_success(id, user_to_delete)

        else:
            user_not_found(id)

    except KeyError:
        invalid_token()
