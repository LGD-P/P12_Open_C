from epic_events.models.models import User
from epic_events.views.users_view import (
    param_not_required, users_table, created_succes, deleted_success, user_not_found,
    param_required, invalid_email, invalid_pass, invalid_role, modification_done,
    input_old_pass, wrong_pass, new_pass, username_not_found, login_success)
import re
import passlib.hash
import click
from sqlalchemy import select
import jwt
import secrets
from dotenv import find_dotenv
import os


@click.group()
@click.pass_context
def user(ctx):
    pass


def pass_is_valid(ctx, param, value):
    regex = re.compile(
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
    if value != ctx.params.get('password', None) and re.fullmatch(regex, value) is None:
        invalid_pass()
        raise click.UsageError(
            "Invalid password. Passwords do not match or not strong enough.")
    return value


def change_password(user_to_modify, ctx):
    initial_password = input_old_pass()
    checking = passlib.hash.argon2.verify(
        initial_password, user_to_modify.password)

    if not checking:
        wrong_pass()
        raise click.UsageError("Password does not match with user.")

    new_password = new_pass()
    pass_is_valid(ctx, param=None, value=new_password)

    new_password = passlib.hash.argon2.using(rounds=12).hash(new_password)

    repete_password = new_pass()
    confirmed = passlib.hash.argon2.verify(repete_password, new_password)

    if not confirmed:
        wrong_pass()
        raise click.UsageError("You confirmed a wrong password.")

    return new_password


def email_is_valid(ctx, param, value):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, value):
        return value
    else:
        invalid_email()
        raise click.UsageError("Invalid email.")


def role_is_valid(ctx, param, value):

    if value in ["support", "commercial", "management"]:
        return value
    else:
        invalid_role()
        raise click.UsageError("Invalid role")


@user.command()
@click.option('--id', '-i', help='Id of the user to query')
@click.pass_context
def list(ctx, id):
    session = ctx.obj['session']

    if id:
        user = session.scalar(select(User).where(User.id == id))
        print(user.password)
        if user is None:
            user_not_found(id)
        else:
            users_table([user])

    else:
        users_list = session.scalars(
            select(User).order_by(User.id)).all()

        users_table(users_list)


@user.command()
@click.option('--name', '-n', help='Name for the new object', required=True)
@click.option('--email', '-e', help='Email for the new object', required=True, callback=email_is_valid)
@click.option('--role', '-r', help='Role must be : support management or commercial', required=True, callback=role_is_valid)
@click.option('--password', '-P', help='Password will automaticly be asked don\'t use this option',
              prompt=True, hide_input=True, confirmation_prompt=True, default=None,
              callback=pass_is_valid)
@click.pass_context
def create(ctx, name, email, role, password):
    session = ctx.obj['session']

    if not name or not email or not role:
        param_required()

    if password is not None:
        param_not_required()
        raise click.UsageError(
            "The '-P' option is not required. Password will automaticly be asked don\'t use this option")
    else:

        hashed_password = passlib.hash.argon2.using(
            rounds=12).hash(password)

        new_user = User(name=name, email=email,
                        role=role, password=hashed_password)
        session.add(new_user)
        session.commit()
        created_succes(new_user)

    session.close()


@user.command()
@click.option('--id', '-i', help='Id of the user you want to modify', required=True)
@click.option('--name', '-n', help='New name of the user')
@click.option('--email', '-e', help='New email of the user')
@click.option('--role', '-r', help='New role of the user, must be: support management or commercial')
@click.option('--password', '-P', help='-P without argument', nargs=0)
@click.pass_context
def modify(ctx, id, name, email, role, password):
    session = ctx.obj['session']

    user_to_modify = session.scalar(select(User).where(User.id == id))
    if user_to_modify:

        if name is not None:
            user_to_modify.name = name

        if email is not None:
            email = email_is_valid(ctx, None, email)
            user_to_modify.email = email

        if role is not None:
            role = role_is_valid(ctx, None, role)
            user_to_modify.role = role

        if password is not None:
            new_password = change_password(user_to_modify, ctx)
            user_to_modify.password = new_password

        session.commit()
        modification_done(user_to_modify)
    else:
        user_not_found(id)
    session.close()


@user.command()
@click.option('--id', '-i', help='Id of the user you want to delete', required=True)
@click.pass_context
def delete(ctx, id):
    session = ctx.obj['session']

    user_to_delete = session.scalar(select(User).where(User.id == id))

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        deleted_success(id, user_to_delete)

    else:
        user_not_found(id)

    session.close()


def update_secret_key_in_env_file(secret_key):
    pass


def generate_token(user_info, secret_key):
    token = jwt.encode(user_info, secret_key, algorithm='HS256')
    return token


@user.command()
@click.option('--name', '-n', help='Id of the user you want to delete', required=True)
@click.option('--password', '-P', help='Password of the user you want to delete', nargs=0)
@click.pass_context
def login(ctx, name, password):
    session = ctx.obj['session']

    user = session.scalar(select(User).where(User.name == name))
    if user:
        pass_to_check = new_pass()
        checking = passlib.hash.argon2.verify(
            pass_to_check, user.password)
        login_success(user.name)

        paylod = {
            'username': user.name,
            'email': user.email,
            'role': user.role
        }
        secret_key = secrets.token_hex(16)

        token = generate_token(paylod, secret_key)

        upadte_secret = update_secret_key_in_env_file(secret_key)

        if not checking:
            wrong_pass()
            raise click.UsageError("Password does not match with user.")
    else:
        username_not_found(name)
        raise click.UsageError("User not found.")
    session.close()
