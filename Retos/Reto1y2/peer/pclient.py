import os
import sys
import time
from threading import Thread

import dotenv
import grpc
import pserver_pb2
import pserver_pb2_grpc

from pserver import login, pserver, query_file, upload_file

env_path = os.path.join(os.path.dirname(__file__),
                        f"../bootstrap/.env_{sys.argv[1]}")
dotenv.load_dotenv(dotenv_path=env_path)

PSERVER_PORT = os.getenv("PSERVER_PORT")
PSERVER_URL = os.getenv("PSERVER_URL")


def login_to_server():
    username = input("Enter username: ")
    password = input("Enter password: ")
    pclient_data = {"username": username, "password": password}
    response = login(pclient_data)
    while response.status_code == 401:
        print("Invalid credentials")
        username = input("Enter username: ")
        password = input("Enter password: ")
        pclient_data = {"username": username, "password": password}
        response = login(pclient_data)
    print(f"Logged in as {username}")


if __name__ == "__main__":
    grpc_channel = grpc.insecure_channel(f"{PSERVER_URL}:{PSERVER_PORT}")
    stub = pserver_pb2_grpc.PServerStub(grpc_channel)
    pserver_thread = Thread(target=pserver)
    pserver_thread.start()
    login_to_server()
    while True:
        print("\nWhat do you want to do?")
        print("1. Upload file")
        print("2. Download file")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            file_name = input("Enter file name: ")
            response = stub.UploadFile(
                pserver_pb2.File(file_name=file_name))
            if response.status_code == 200:
                print("File uploaded")
            elif response.status_code == 409:
                print("File already exists")
        elif choice == "2":
            file_name = input("Enter file name: ")
            response = stub.DownloadFile(
                pserver_pb2.File(file_name=file_name))
            if response.status_code == 200:
                print("File downloaded")
            elif response.status_code == 404:
                print("File not found")
        elif choice == "3":
            break
