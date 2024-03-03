"""
This file contains the server code for the PServer
"""
import json
import os
import random
from threading import Thread
import time

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "../bootstrap/.env_server")
load_dotenv(dotenv_path=env_path)

SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

app = Flask(__name__)

# Initialize the data structures
users = {}
urls = {}
files = {}
active_peers = {}


@app.route("/login", methods=["POST"])
def login():
    """
    Login to the server
    :return: Response
    """
    pserver_data = request.json
    username = pserver_data.get("username")
    password = pserver_data.get("password")
    url = pserver_data.get("url")
    if username in users:
        if users[username] == password:
            urls[username] = url
            return Response(status=200)
    else:
        users[username] = password
        urls[username] = url
        return Response(status=200)
    return Response(status=401)


@app.route("/logout", methods=["POST"])
def logout():
    """
    Logout from the server
    :return: Response
    """
    pserver_data = request.json
    username = pserver_data.get("username")
    if username in users:
        del active_peers[urls[username]]
        del users[username]
        del urls[username]
        return Response(status=200)
    return Response(status=401)


@app.route("/query", methods=["GET"])
def query():
    """
    Query the server for the file urls
    :return: Response
    """
    pserver_data = request.json
    file_name = pserver_data.get("file_name")
    if file_name in files:
        file_urls = files[file_name]
        return jsonify(file_urls), 200, {'Content-Type': 'application/json'}
    return Response(status=404)


@app.route("/index", methods=["POST"])
def index():
    """
    Index the file urls
    :return: Response
    """
    pserver_data = request.json
    pserver_files = pserver_data.get("files")
    url = pserver_data.get("url")
    if pserver_files is None:
        return Response(status=200)
    for file_name in pserver_files:
        if file_name in files and url not in files[file_name]:
            files[file_name].append(url)
            return Response(status=200)
    files[file_name] = [url]
    return Response(status=200)


@app.route("/upload", methods=["GET"])
def upload():
    """
    Upload the file urls
    :return: Response or str
    """
    pserver_data = request.json
    url = get_peer(pserver_data.get("url"))
    if url is None:
        return Response(status=404)
    return jsonify(url), 200, {'Content-Type': 'application/json'}


@app.route("/ping", methods=["GET"])
def ping():
    """
    Ping the server
    :return: Response
    """
    pserver_data = request.json
    url = pserver_data.get("url")
    time_stamp = pserver_data.get("time_stamp")
    active_peers[url] = time_stamp
    return Response(status=200)


def check_active_peers():
    """
    Check the active peers
    :return: None
    """
    for peer in active_peers:
        if time.time() - active_peers[peer] > 15:
            del active_peers[peer]
            if peer in urls:
                del urls[peer]


def get_peer(url):
    """
    Get the peer to upload the file
    :param url: str
    :return: Response or str
    """
    if len(active_peers) == 1:
        return None
    peers = list(active_peers.keys())
    random_peer = random.choice(peers)
    while random_peer == url:
        random_peer = random.choice(peers)
    return random_peer


if __name__ == "__main__":
    Thread(target=check_active_peers).start()
    app.run(host=SERVER_URL, port=SERVER_PORT, debug=True)
