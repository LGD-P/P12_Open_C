from epic_events.models.user import User
from epic_events.views.users_view import expired_token
from sqlalchemy import select

import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


load_dotenv()


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

    file_path = os.path.join(folder_path, 'temporary.txt')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.listdir(folder_path):
        with open(file_path, 'w') as file:
            file.write(f"TOKEN={token}\n")
    else:
        for filename in os.listdir(folder_path):
            file_path_to_delete = os.path.join(folder_path, filename)
            os.unlink(file_path_to_delete)

        with open(file_path, 'w') as file:
            file.write(f"TOKEN={token}\n")


def check_authentication(func):
    def _get_user(session):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        temp_path = os.environ.get("TEMP_TOKEN_PATH")
        token = os.path.join(
            script_directory, temp_path)

        if not os.path.exists(token) or not os.path.isfile(token):
            expired_token()
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

    def if_token_valid(ctx, *args, **kwargs):
        ctx.ensure_object(dict)
        user_id = _get_user(ctx.obj['session'])
        if user_id:
            ctx.obj['user_id'] = user_id
        return func(ctx, *args, **kwargs)
    return if_token_valid
