#FastAPI server
#New update
import base64
import json
from datetime import datetime
from fastapi import Body, FastAPI, Cookie, Request
from fastapi.responses import Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from utils import authentication, try_authenticate_user, verify_password, users, sign_data


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index_page(request: Request, username: Optional[str] = Cookie(default=None)):
    data = authentication(username)
    data['section'] = 'updates'
    return templates.TemplateResponse("index_page.html", {'request': request, 'data': data})


@app.get("/login")
def login_page(request: Request, username: Optional[str] = Cookie(default=None)):

    if not username:
        data = {
            'authenticated': False,
        }
        return templates.TemplateResponse("login.html", {'request': request, 'data': data})
    
    user = try_authenticate_user(username)
    if user:
        return RedirectResponse("/")
    else:
        data = {
            'authenticated': False
        }
        response = templates.TemplateResponse("login.html", {'request': request, 'data': data})
        response.delete_cookie(key="username")
        return response


@app.post("/login")
def login_process(data: dict = Body(...)):
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


@app.post('/logout')
def logout_process():
    response = Response(
        json.dumps({
            "success": True
            }), media_type="application/json")
    response.delete_cookie(key="username")
    return response


@app.get('/lab1')
def lab1(request: Request, username: Optional[str] = Cookie(default=None)):
    data = authentication(username)
    return templates.TemplateResponse("lab1.html", {'request': request, 'data': data})


@app.get("/services")
def services(request: Request, username: Optional[str] = Cookie(default=None)):
    data = authentication(username)
    data['section'] = 'services'
    return templates.TemplateResponse("services.html", {'request': request, 'data': data})


@app.get("/projects")
def services(request: Request, username: Optional[str] = Cookie(default=None)):
    data = authentication(username)
    data['section'] = 'projects'
    return templates.TemplateResponse("projects.html", {'request': request, 'data': data})


@app.get("/contacts")
def services(request: Request, username: Optional[str] = Cookie(default=None)):
    data = authentication(username)
    data['section'] = 'contacts'
    return templates.TemplateResponse("contacts.html", {'request': request, 'data': data})




@app.get("/question")
def q1(request: Request):
    return templates.TemplateResponse("quest.html", {'request': request})






@app.post("/question_review")
def review_answer(data: dict = Body(...)):
    answer = str(data["answer"]).lower().replace(" ", "")
    with open('file.txt', 'a') as f: 
        f.write(str(datetime.now()) + ' ' + answer + '\n')
    with open('messages.json', 'r') as f:
        answers = json.load(f)
    if answer in answers:
        response = Response(
            json.dumps({
                "success": True,
                "message": answers[answer]
                }), media_type="application/json")
    else:
        response = Response(
        json.dumps({
            "success": False,
            "message": "ДУХ говорит, <br> ответ неверный "
            }), media_type="application/json")
    return response