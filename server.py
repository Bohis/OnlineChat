import socket
import threading
from authorize import Authorize_servis
from client_data import Client
from messageRouter import MessageRouter
from config import *

lock = threading.Lock()
clients_socket = []
theard_list = []

ip_host, port = load_data_config(PATH_CONFIG)
clients_data:dict[str, Client] = {client.login:client for client in load_data_clients(PATH_CLIENTS)} 

authorize_handle = Authorize_servis(clients_data)
message_router = MessageRouter(clients_data)

def disconnect_handle(connection_socket: socket.socket, addres: str):
    print(f"[-] disconnect {addres}")
        
    with lock:
        clients_socket.remove(connection_socket)
        
    connection_socket.close()

def handle_client(connection_socket: socket.socket, addres:str):
    print(f"[+] client try connect {addres}")
    
    auth_data = ""
    client = None
    
    while True:
        try:
            auth_data += connection_socket.recv(1024).decode("utf-8")
            if auth_data.endswith("|"):
                auth_data = auth_data[:-1]
                
                login, password = auth_data.split("\n")
                
                if authorize_handle.check_client_login_and_password(login, password):
                    message_router.route_callback_to_socket(connection_socket, f"COMMAND:{SUCCES_AUTHORIZE}")
                    print(f"[+] client {addres} authorized")
                    client = clients_data[login]
                    with lock:
                        client.ip = addres
                        client.socket_client = connection_socket
                    break
                else:
                    message_router.route_callback_to_socket(connection_socket, f"COMMAND:{ERROR_AUTHORIZE}")
                    print(f"[-] client {addres} wrong login or password")
                
        except BaseException as error:
            print(f"[error] error input {error}")
            message_router.route_callback_to_socket(connection_socket, "authorized error. Repeat input")
            
    
    while True:
        data = ""
        while True:
            try:
                data += connection_socket.recv(1024).decode("utf-8")
                if data.endswith("|"):
                    data = data[:-1]
                    print(f"[+] accept message {repr(data)} from {addres}")
                    break
            except:
                disconnect_handle(connection_socket, addres)
                return 
        
        from_client, to_client, message = data.split("\n")
        send_mesage_from_client_to_client(clients_data.get(from_client), clients_data.get(to_client), message)

def send_mesage_from_client_to_client(from_client:Client, to_client:Client, message:str):
    if to_client in clients_data.values():
        message_router.route_send_message(from_client, to_client, message)
        message_router.route_callback(from_client, f"COMMAND:{SUCCES_SEND}")
    else:
        message_router.route_callback(from_client, f"COMMAND:{ERROR_SEND}")
        print(f"[error] client {to_client.login} not found")

def start_server():
    socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_chat.bind((ip_host, port))
    socket_chat.listen()
    print(f"[*] start server {ip_host}:{port}")
    
    while True:
        connection_socket, addres = socket_chat.accept()
        clients_socket.append(connection_socket)
        thread = threading.Thread(target = handle_client, args= (connection_socket, addres))
        thread.start()
        theard_list.append(thread)

if __name__ == "__main__":
    start_server()