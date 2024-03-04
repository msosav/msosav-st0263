import os
import sys
import time
from concurrent import futures

import dotenv
import grpc
import pserver_pb2
import pserver_pb2_grpc
import requests
from threading import Thread

env_path = os.path.join(os.path.dirname(__file__), sys.argv[2])
dotenv.load_dotenv(dotenv_path=env_path)

PSERVER_PORT = os.getenv("PSERVER_PORT")
PSERVER_URL = os.getenv("PSERVER_URL")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")

files = []
ping_status = True


def pserver():
    """
    Start the pserver
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f"{PSERVER_URL}:{PSERVER_PORT}")
    pserver_pb2_grpc.add_PServerServicer_to_server(PServerServicer(), server)
    server.start()
    server.wait_for_termination()


def login(pclient_data):
    """
    Login to the server
    :param pclient_data: dict
    :return: Response
    """
    username = pclient_data.get("username")
    password = pclient_data.get("password")
    url = f"{PSERVER_URL}:{PSERVER_PORT}"
    pserver_data = {"username": username, "password": password, "url": url}
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/login", json=pserver_data
    )
    return response


def upload_file(file_name):
    """
    Upload file to the server
    :param file_name: str
    :return: Response
    """
    url = f"{PSERVER_URL}:{PSERVER_PORT}"
    pserver_data = {"file_name": file_name, "url": url}
    response = requests.get(
        f"http://{SERVER_URL}:{SERVER_PORT}/upload", json=pserver_data
    )
    return response


def query_file(file_name):
    """
    Query the server for the file urls
    :param file_name: str
    :return: Response
    """
    pserver_data = {"file_name": file_name}
    response = requests.get(
        f"http://{SERVER_URL}:{SERVER_PORT}/query", json=pserver_data
    )
    return response


def send_index():
    """
    Send the index to the server
    :return: Response
    """
    pserver_data = {"files": files, "url": f"{PSERVER_URL}:{PSERVER_PORT}"}
    response = requests.post(
        f"http://{SERVER_URL}:{SERVER_PORT}/index", json=pserver_data)
    return response


def file_already_exists(file_name):
    """
    Check if the file already exists
    :param file_name: str
    :return: bool
    """
    return file_name in files


def ping():
    """
    Ping the server
    :return: None
    """
    global ping_status
    while ping_status:
        response = requests.get(
            f"http://{SERVER_URL}:{SERVER_PORT}/ping",
            json={"url": f"{PSERVER_URL}:{PSERVER_PORT}",
                  "time_stamp": time.time()}
        )
        time.sleep(10)


class PServerServicer(pserver_pb2_grpc.PServerServicer):
    """
    PServerServicer class
    """

    def Login(self, request, context):
        global ping_status
        ping_status = True
        Thread(target=ping).start()
        username = request.username
        password = request.password
        response = login({"username": username, "password": password})
        return pserver_pb2.Response(status_code=response.status_code)

    def Logout(self, request, context):
        global ping_status
        ping_status = False
        username = request.username
        response = requests.post(
            f"http://{SERVER_URL}:{SERVER_PORT}/logout",
            json={"username": username}
        )
        return pserver_pb2.Response(status_code=response.status_code)

    def DownloadFileRequest(self, request, context):
        file_name = request.file_name
        if file_already_exists(file_name):
            return pserver_pb2.Response(status_code=409)
        response = query_file(file_name)
        if response.status_code == 200:
            channel = grpc.insecure_channel(response.json()[0])
            stub = pserver_pb2_grpc.PServerStub(channel)
            response = stub.DownloadFile(pserver_pb2.File(file_name=file_name))
            if response.status_code == 200:
                files.append(file_name)
                send_index()
                return response
        else:
            response = pserver_pb2.Response()
            response.status_code = 404
            return response
        response = pserver_pb2.Response()
        response.status_code = 404
        return response

    def DownloadFile(self, request, context):
        file_name = request.file_name
        if file_name in files:
            response = pserver_pb2.Response()
            response.status_code = 200
            return response
        response = pserver_pb2.Response()
        response.status_code = 404
        return response

    def UploadFileRequest(self, request, context):
        file_name = request.file_name
        if file_already_exists(file_name):
            return pserver_pb2.Response(status_code=409)
        response = upload_file(file_name)
        if response.status_code == 200:
            channel = grpc.insecure_channel(response.json())
            stub = pserver_pb2_grpc.PServerStub(channel)
            response = stub.UploadFile(pserver_pb2.File(file_name=file_name))
            if response.status_code == 200:
                return response
        return pserver_pb2.Response(status_code=404)

    def UploadFile(self, request, context):
        file_name = request.file_name
        if file_name not in files:
            files.append(file_name)
        send_index()
        return pserver_pb2.Response(status_code=200)


if __name__ == "__main__":
    pserver()
