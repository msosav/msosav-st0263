import os
import sys
import time
from concurrent import futures
from threading import Thread

import dotenv
import grpc
import requests
from flask import Flask

import pserver_pb2
import pserver_pb2_grpc

app = Flask(__name__)

env_path = os.path.join(os.path.dirname(__file__),
                        f"../bootstrap/.env_{sys.argv[2]}")
dotenv.load_dotenv(dotenv_path=env_path)

PSERVER_PORT = os.getenv("PSERVER_PORT")
PSERVER_URL = os.getenv("PSERVER_URL")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

files = []


def pserver():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f"{PSERVER_URL}:{PSERVER_PORT}")
    pserver_pb2_grpc.add_PServerServicer_to_server(PServerServicer(), server)
    server.start()
    server.wait_for_termination()


def login(pclient_data):
    username = pclient_data.get("username")
    password = pclient_data.get("password")
    url = f"{PSERVER_URL}:{PSERVER_PORT}"
    pserver_data = {"username": username, "password": password, "url": url}
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/login", json=pserver_data
    )
    return response


def upload_file(file_name):
    url = f"{PSERVER_URL}:{PSERVER_PORT}"
    pserver_data = {"file_name": file_name, "url": url}
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/upload", json=pserver_data
    )
    return response


def query_file(file_name):
    pserver_data = {"file_name": file_name}
    response = requests.get(
        f"http://{SERVER_URL}:{SERVER_PORT}/query", json=pserver_data
    )
    return response


def send_index():
    pserver_data = {"files": files, "url": f"{PSERVER_URL}:{PSERVER_PORT}"}
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/index", json=pserver_data)
    return response.status_code


class PServerServicer(pserver_pb2_grpc.PServerServicer):
    def DownloadFile(self, request, context):
        file_name = request.file_name
        response = query_file(file_name)
        if response.status_code == 200:
            channel = grpc.insecure_channel(response.json()[0])
            stub = pserver_pb2_grpc.PServerStub(channel)
            response = stub.RequestFile(pserver_pb2.File(file_name=file_name))
            if response.status_code == 200:
                return response
            else:
                response = pserver_pb2.Response()
                response.status_code = 404
                return response
        else:
            response = pserver_pb2.Response()
            response.status_code = 404
            return response

    def RequestFile(self, request, context):
        file_name = request.file_name
        if file_name in files:
            response = pserver_pb2.Response()
            response.status_code = 200
            return response
        else:
            response = pserver_pb2.Response()
            response.status_code = 404
            return response

    def UploadFile(self, request, context):
        file_name = request.file_name
        response = upload_file(file_name)
        if response.status_code == 200:
            response = pserver_pb2.Response()
            response.status_code = 200
            files.append(file_name)
            return response
        else:
            response = pserver_pb2.Response()
            response.status_code = 409
            return response


if __name__ == "__main__":
    pserver()
