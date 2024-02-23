import os
from dotenv import load_dotenv
import sys

from flask import Flask, request
import json

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "../bootstrap/.env_server")
load_dotenv(dotenv_path=env_path)

SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

app = Flask(__name__)

users = {}
files = {}


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/login', methods=['GET'])
def login():
    pserver_data = request.args
    username = pserver_data.get('username')
    password = pserver_data.get('password')
    if username in users and users[username] == password:
        pserver_data = {"username": username}
        return json.dumps(pserver_data)  # Convertir a JSON y retornar
    elif username in users and users[username] != password:
        return "Invalid password"
    else:
        users[username] = password
        pserver_data = {"username": username}
        return json.dumps(pserver_data)  # Convertir a JSON y retornar


@app.route('/upload', methods=['POST'])
def upload():
    pserver_data = request.json
    url = pserver_data.get('url')
    file_name = pserver_data.get('file_name')
    if file_name in files:
        if files[file_name] == url:
            return f"File already uploaded by you"
        else:
            files[file_name] = [files[file_name], url]
    else:
        files[file_name] = url
    return f"File uploaded successfully"


@app.route('/download', methods=['GET'])
def download():
    pserver_data = request.json
    file_name = pserver_data.get('file_name')
    if file_name in files:
        return f"File available at {files[file_name]}"
    else:
        return f"File not available"


if __name__ == "__main__":
    app.run(host=SERVER_URL, port=SERVER_PORT, debug=True)
