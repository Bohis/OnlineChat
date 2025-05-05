import socket
import threading
import json
import os
from client_data import Client

PATH_CONFIG = os.path.join(os.path.dirname(__file__), "config.json")
PATH_CLIENTS = os.path.join(os.path.dirname(__file__), "clients.json")

def load_data_config(path:str) -> tuple[str, str]:
    with open(path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        return data["host_ip"], int(data["port"])
    
    return None

def load_data_clients(path:str) -> list[Client]:
    with open(path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        client_data = [Client(data["login"], data["password"]) for data in  data["clients"]]
        
        return client_data
    
    return None

ip_host, port = load_data_config(PATH_CONFIG)
clients_data = load_data_clients(PATH_CLIENTS)

lock = threading.Lock()

clients_data = {client.login:client for client in clients_data}
authorized_clients = {}
clients_now = []

theard_list = []

def handle_client(connection_socket: socket.socket, addres:str):
    print(f"[+] client try connect {addres}")
    auth_data = ""
    while True:
        try:
            auth_data += connection_socket.recv(1024).decode("utf-8")
            if auth_data.endswith("|"):
                auth_data = auth_data.replace("|", "")
                break
        except BaseException as error:
            print(f"[error] error input {error}")
            break
    
    auth_data = auth_data.split("\n")
    
    if not(len(auth_data) == 2 and auth_data[0] in clients_data and clients_data[auth_data[0]].password == auth_data[1]):
        print(f"[-] disconnect {addres}")
        
        with lock:
            clients_now.remove(connection_socket)
            
        connection_socket.close()
        return
    
    print(f"[-] client {addres} authorized")
    client = clients_data[auth_data[0]]
    with lock:
        client.ip = addres
        authorized_clients[addres] = connection_socket
    
    while True:
        data = ""
        while True:
            try:
                data += connection_socket.recv(1024).decode("utf-8")
                if data.endswith("|"):
                    data = data.replace("|", "")
                    print(f"[+] accept message {data}")
                    break
            except:
                print(f"[-] disconnect {addres}")
                
                with lock:
                    clients_now.remove(connection_socket)
                    authorized_clients.pop(client.ip)
                    
                connection_socket.close()
                return 
        
        
        from_client, to_client, message = data.split("\n")
        print(authorized_clients)
        print(clients_data[to_client].ip)
        print(authorized_clients[clients_data[to_client].ip])
        translate_meassage(authorized_clients[clients_data[to_client].ip], f"{from_client}: {message}")
        
def translate_meassage(to_client:socket.socket, message:str):
    to_client.send(message.encode())
        
def start_server():
    socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_chat.bind((ip_host, port))
    socket_chat.listen()
    print(f"[*] start server {ip_host}:{port}")
    
    while True:
        connection_socket, addres = socket_chat.accept()
        clients_now.append(connection_socket)
        thread = threading.Thread(target = handle_client, args= (connection_socket, addres))
        thread.start()
        theard_list.append(thread)

if __name__ == "__main__":
    start_server()