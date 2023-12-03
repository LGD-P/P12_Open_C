from functools import wraps
from epic_events.models.user import User
from epic_events.models.role import Role
from epic_events.models.client import Client
from epic_events.views.clients_views import client_not_found
from epic_events.views.contracts_views import contract_not_found
from epic_events.views.users_view import not_authorized, user_not_found, invalid_token
from sqlalchemy import select

import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()


def find_client_or_contract(ctx, Client_or_contract_class, client_or_contact_arg):
    session = ctx.obj['session']
    client_or_contact_list = session.scalars(
        select(Client_or_contract_class).order_by(Client_or_contract_class.id)).all()
    for element in client_or_contact_list:
        if element.id == int(client_or_contact_arg):
            return element.id

    if Client_or_contract_class == Client:
        raise ValueError(client_not_found(client_or_contact_arg))
    else:
        raise ValueError(contract_not_found(client_or_contact_arg))


def find_user_type(ctx, user_type, str_user_type):
    session = ctx.obj['session']
    user_type_list = session.scalars(select(User).order_by(User.id)).all()
    for element in user_type_list:
        if element.id == int(user_type) and element.role.name == str_user_type:
            return element.id  #
    raise ValueError(user_not_found(user_type))


def generate_token(user):
    payload = {
        'user_id': user.id,
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=21600)
    }
    secret = os.environ.get("SECRET_KEY")

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def write_token_in_temp(token):
    folder_path = 'temp'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.environ.get("TEMP_TOKEN_PATH"):
        token_path = os.environ.get("TEMP_TOKEN_PATH")

        if os.path.exists(token_path):
            os.remove(token_path)

        with open(token_path, 'w') as file:
            file.write(f"TOKEN={token}\n")


def check_token_to_get_user(session):
    token = os.environ.get("TEMP_TOKEN_PATH")

    if not os.path.exists(token) or not os.path.isfile(token):
        return None

    with open(token, "r") as f:
        for line in f:
            if line.startswith("TOKEN="):
                token = line.split("=", 1)[1].strip()
                secret = os.environ.get("SECRET_KEY")

            if token is None:
                return None

            try:
                decode = jwt.decode(token, secret, algorithms=["HS256"])
                user_id = decode['user_id']
                user = session.scalar(
                    select(User).where(User.id == user_id))
                return user

            except jwt.exceptions.DecodeError:
                return None

            except jwt.exceptions.ExpiredSignatureError:
                return None


def has_permission(allowed_roles):
    def decorator(function):
        @wraps(function)
        def wrapper(ctx, *args, **kwargs):
            ctx.ensure_object(dict)
            session = ctx.obj['session']
            try:
                role_id = ctx.obj["user_id"].role_id
                user_role = session.scalar(
                    select(Role).where(Role.id == role_id))
                if user_role.name not in allowed_roles:
                    return not_authorized()
            except KeyError:
                return invalid_token()
            return function(ctx, *args, **kwargs)

        return wrapper

    return decorator
