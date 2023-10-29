import jwt
import os


def generate_token(user_info, secret_key):
    token = jwt.encode(user_info, secret_key, algorithm='HS256')
    return token


def get_token_in_temp(token):
    folder_path = 'temp'

    file_path = os.path.join(folder_path, 'temporary_t.txt')

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
