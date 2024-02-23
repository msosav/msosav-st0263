from flask import Flask, request
import json
import requests
import os
import sys
import dotenv


env_path = os.path.join(os.path.dirname(__file__),
                        f"../bootstrap/.env_{sys.argv[1]}")
dotenv.load_dotenv(dotenv_path=env_path)

PCLIENT_URL = os.getenv("PCLIENT_URL")
PCLIENT_PORT = os.getenv("PCLIENT_PORT")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

app = Flask(__name__)


def pserver():
    app.run(host=PCLIENT_URL, port=PCLIENT_PORT)


def login(pserver_data):
    username = pserver_data.get('username')
    password = pserver_data.get('password')
    response = requests.get(
        f"http://{SERVER_URL}:{SERVER_PORT}/login?username={username}&password={password}")
    if response.status_code == 200:
        return response.text
    return "Server not available"


def upload_file(pserver_data):
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/upload", json=pserver_data)
    return response.text
