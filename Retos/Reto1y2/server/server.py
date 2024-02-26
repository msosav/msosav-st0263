import json
import os

from dotenv import load_dotenv
from flask import Flask, request, Response, jsonify

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "../bootstrap/.env_server")
load_dotenv(dotenv_path=env_path)

SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

app = Flask(__name__)

users = {}
urls = {}
files = {}


@app.route("/login", methods=["POST"])
def login():
    pserver_data = request.json
    username = pserver_data.get("username")
    password = pserver_data.get("password")
    url = pserver_data.get("url")
    if username in users:
        if users[username] == password:
            urls[username] = url
            return Response(status=200)
        else:
            return Response(status=401)
    else:
        users[username] = password
        urls[username] = url
        return Response(status=200)


@app.route("/query", methods=["GET"])
def query():
    pserver_data = request.json
    file_name = pserver_data.get("file_name")
    if file_name in files:
        file_urls = files[file_name]
        print(json.dumps(file_urls))
        return jsonify(file_urls), 200, {'Content-Type': 'application/json'}
    else:
        return Response(status=404)


@app.route("/index", methods=["POST"])
def index():
    pserver_data = request.json
    pserver_files = pserver_data.get("files")
    url = pserver_data.get("url")
    for file_name in pserver_files:
        if file_name in files and url not in files[file_name]:
            files[file_name].append(url)
            return Response(status=200)


@app.route("/upload", methods=["POST"])
def upload():
    pserver_data = request.json
    file_name = pserver_data.get("file_name")
    url = pserver_data.get("url")
    if file_name in files and url not in files[file_name]:
        files[file_name].append(url)
        return Response(status=200)
    elif file_name in files and url in files[file_name]:
        return Response(status=409)
    else:
        files[file_name] = [url]
        return Response(status=200)


if __name__ == "__main__":
    app.run(host=SERVER_URL, port=SERVER_PORT, debug=True)
