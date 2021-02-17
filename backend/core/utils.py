import hashlib


def hash_password(password: str):
    hashed_password = hashlib.sha1(password.encode('utf-8'))
    return hashed_password.hexdigest()
