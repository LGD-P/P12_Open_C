from epic_events.views.users_view import invalid_token

import jwt
import os
from datetime import datetime, timedelta, timezone


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


def is_token_valid():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    token = os.path.join(
        script_directory, "/home/lgd-/Documents/Open_C/Original/P12_Open_C/P12_Open_C/epic_events/temp/temporary.txt")

    with open(token, "r") as f:
        for line in f:
            if line.startswith("TOKEN="):
                token = line.split("=", 1)[1].strip()
                secret = os.environ.get("SECRET_KEY")

            try:
                decode = jwt.decode(token, secret, algorithms=["HS256"])

                return decode['user_id']

            except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
                invalid_token()
