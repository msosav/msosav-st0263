"""
This file contains the client code for the pserver. It uses gRPC to communicate with the pserver.
"""
import os
import sys
from threading import Thread

import dotenv
import grpc
import pserver_pb2
import pserver_pb2_grpc
from pserver import pserver

env_path = os.path.join(os.path.dirname(__file__), sys.argv[1])
dotenv.load_dotenv(dotenv_path=env_path)

PSERVER_PORT = os.getenv("PSERVER_PORT")
PSERVER_URL = os.getenv("PSERVER_URL")


def login_to_server(stub):
    """
    Login to the server
    :param stub: PServerStub
    :return: None
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = stub.Login(pserver_pb2.UserData(
        username=username, password=password))
    while response.status_code == 401:
        print("Invalid credentials")
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = stub.Login(pserver_pb2.UserData(
            username=username, password=password))
    print(f"Logged in as {username}")
    return username


if __name__ == "__main__":
    grpc_channel = grpc.insecure_channel(f"{PSERVER_URL}:{PSERVER_PORT}")
    stub = pserver_pb2_grpc.PServerStub(grpc_channel)
    pserver_thread = Thread(target=pserver)
    pserver_thread.start()
    while True:
        username = login_to_server(stub)
        while True:
            print("\nWhat do you want to do?")
            print("1. Upload file")
            print("2. Download file")
            print("3. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                file_name = input("Enter file name: ")
                response = stub.UploadFileRequest(
                    pserver_pb2.File(file_name=file_name))
                if response.status_code == 200:
                    print("\nFile uploaded")
                elif response.status_code == 404:
                    print("\nNo active peers available to upload file to")
                elif response.status_code == 409:
                    print("\nFile already exists")
            elif choice == "2":
                file_name = input("Enter file name: ")
                response = stub.DownloadFileRequest(
                    pserver_pb2.File(file_name=file_name))
                if response.status_code == 200:
                    print("\nFile downloaded")
                elif response.status_code == 404:
                    print("\nFile not found")
                elif response.status_code == 409:
                    print("\nFile already exists in the peer directory")
            elif choice == "3":
                response = stub.Logout(pserver_pb2.Username(username=username))
                if response.status_code == 200:
                    print("Logged out")
                    break
                break
