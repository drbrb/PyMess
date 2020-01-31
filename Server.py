import time
from flask import Flask, request
import datetime

app = Flask(__name__)
messages = [
    {"username": "Jack", "text": "Hello!", "time": time.time()},
    {"username": "Marry", "text": "Hello!", "time": time.time()}
]
users = {
    "Jack": "12345",
    "Mary": "12345"
}


@app.route("/")
def hello_view():
    return "Hello <h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    status = {"status": True, "Datetime": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    return f'I am live! Status : {status["status"]}, ' \
           f'current time: {status["Datetime"]}'


@app.route("/messages")
def messages_view():
    """
    Получение сообщений после отметки after
    input: after - отметка времени
    output: {
    "messages":[
    {"username":str, "text": str, "time": float}
    ...
        ]
     }
    """
    after = float(request.args['after'])

    # new_messages = []
    # for message in messages:
    #     if message["time"]> after:
    #         new_messages.append(message)
    new_messages = [message for message in messages if message["time"] > after]
    return {'messages': new_messages}


@app.route("/send", methods=['POST'])
def send():
    """
    Передача сообщения
    input: {
    "messages":[
    {"username":str, "text": str, time: float}
    ]... }
    output: {'ok': True}
    """
    data = request.json

    username = data["username"]
    text = data["text"]

    messages.append({"username": username, "text": text, "time": time.time()})
    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Авторизовать пользователя или сообщить, что пароль не верный
    input: {
    "username":str,
     "password": str
     }
    output: {'ok': bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]
    if username not in users:
        users[username] = password
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


app.run()
