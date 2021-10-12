import base64
import hmac
import hashlib
from typing import Optional, Union


SECRET_KEY = "a2ed9baa08cbcf3b6b22616b66ce1ffd92495d64a0d6fd39a1ccaf83e9c9731"
PASSWORD_SALT = "db561e1530e281edfef76471f1817cae1facded52bfdbf14215d219e91927fab"

users = {
    'ilya@user.com': {
        'name': 'ilya',
        'password': 'eced9ee1d31eb9b3f71c50e7ef5f3388869782282407faf2242c6a35bbb68345',
        'balance': 100000
        },
    'alexey@user.com': {
        'name': 'Petr',
        'password': 'dd947018864cd617310e56ac3eb52ccd9cf2701a3904e7a7e311b5ba5b498cd0',
        'balance': 555555,
        },
}

def verify_password(username: str, password: str) -> bool:
    """Хэширует введённый пароль и сравнивает с сохраненным хэшем"""
    password_stored = users[username]['password']
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest()
    return password_stored.lower() == password_hash.lower()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    """Возвращает имя пользователя из подписанной строки, если данные корректны"""
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

def try_authenticate_user(username: Union[str, None]) -> Optional[str]:
    if not username:
        return 
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        return 
    try:
        user = users[valid_username]
    except KeyError:
        return
    return user


def sign_data(data: str) -> str:
    """Возвращает подписанные данные data"""
    return hmac.new(
            SECRET_KEY.encode(), 
            msg=data.encode(),
            digestmod=hashlib.sha256
            ).hexdigest().upper()

def authentication(username):
    data = {}
    user = try_authenticate_user(username)
    if user:
        data['authenticated'] = True
        data['name'] = user['name']
    else:
        data['authenticated'] = False
    return data