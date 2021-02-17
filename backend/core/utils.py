import hashlib

import jwt as jwt


def hash_password(password: str):
    hashed_password = hashlib.sha1(password.encode('utf-8'))
    return hashed_password.hexdigest()


def generate_jwt_token(user_dict: dict[str, str]):
    return jwt.encode(user_dict, 'secret', algorithm='HS256')


def decode_jwt_token(token: str):
    return jwt.decode(token, 'secret', algorithms=['HS256'])
