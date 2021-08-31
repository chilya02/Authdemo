#FastAPI server
#New update
import base64
import hmac
import hashlib
import json
from typing import Dict, Optional
from fastapi import Body, FastAPI, Form, Cookie
from fastapi.responses import Response

app = FastAPI()

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

def sign_data(data: str) -> str:
    """Возвращает подписанные данные data"""
    return hmac.new(
            SECRET_KEY.encode(), 
            msg=data.encode(),
            digestmod=hashlib.sha256
            ).hexdigest().upper()


@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()

    if not username:
        return Response(login_page, media_type="text/html")
    
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response 
    
    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")       
        return response

    return Response(f'Привет, {user["name"]}', media_type="text/html")



@app.post("/login")
def process_login_page(data: dict = Body(...)):
    print("data is", data)
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
                json.dumps({
                    "succes": False,
                    "message": "Я вас не знаю",
                    }), media_type="application/json")

    response = Response(
        json.dumps({
            "success": True,
            "message": f'Привет, {user["name"]}<br>, Твой баланс:{user["balance"]}'
            }), media_type="application/json")
    username_signed = base64.b64encode(username.encode()).decode() + "." + \
            sign_data(username)
    response.set_cookie(key="username", value=username_signed)
    return response


@app.post("/unify_phone_from_json")
def parse_phone_from_string(data: dict = Body(...)):
    input_string = data["phone"]
    buf = ''
    for char in input_string:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")


@app.post("/unify_phone_from_form")
def parse_phone_from_form(phone: str = Form(...):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")

@app.get("/unify_phone_from_query")
async def read_item(phone: str):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")


@app.get("/unify_phone_from_cookies")
def parse_phone_from_cookies(phone = Cookie(...)):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")
