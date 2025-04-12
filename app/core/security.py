import hashlib
import os

def get_password_hash(password: str, salt: str = None) -> str:
    if not salt:
        salt = os.urandom(16).hex()
    hash_obj = hashlib.sha256((salt + password).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, hash_val = hashed_password.split("$")
        return get_password_hash(plain_password, salt) == hashed_password
    except ValueError:
        return False
