import dotenv
import os
import sys
import time
from pserver import pserver, login, upload_file, query_file
from threading import Thread
env_path = os.path.join(os.path.dirname(__file__),
                        f"../bootstrap/.env_{sys.argv[1]}")
dotenv.load_dotenv(dotenv_path=env_path)

PCLIENT_URL = os.getenv("PCLIENT_URL")
PCLIENT_PORT = os.getenv("PCLIENT_PORT")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")


def login_to_server():
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {"username": username, "password": password}
    login_response = login(data)
    print(login_response)
    if "Invalid password" in login_response:
        username = input("Enter username: ")
        password = input("Enter password: ")
        data = {"username": username, "password": password}
        login_response = login(data)
        print(login_response)


if __name__ == "__main__":
    url = f"http://{PCLIENT_URL}:{PCLIENT_PORT}"
    pserver_thread = Thread(target=pserver)
    pserver_thread.start()
    time.sleep(2)
    login_to_server()
    while True:
        print("\nWhat do you want to do?")
        print("1. Upload file")
        print("2. Download file")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            file_name = input("Enter file name: ")
            data = {"url": url, "file_name": file_name}
            print(upload_file(data))
        elif choice == "2":
            file_name = input("Enter file name: ")
            data = {"file_name": file_name}
            print(query_file(data))
        elif choice == "3":
            break
