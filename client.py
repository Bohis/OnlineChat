import socket
import threading
from config import *
import time

ip_host, port = load_data_config(PATH_CONFIG)
thread_list = []
authorized = None
callback = True

def chat_activity(socket_server:socket.socket):
    global authorized, callback
    
    while True:
        login = input("enter yor login: ")
        password = input("enter yor password: ")
        socket_server.send(f"{login}\n{password}|".encode('utf-8'))
        
        while authorized == None:
            time.sleep(1)
        
        if authorized:
            print("succes authorize, entering in the chat")
            break
        else:
            print("error authorize, wrong login or password")
            authorized = None
    
    while True:
        if not callback:
            time.sleep(1)
            continue

        login_to_client = input("login: ")
        message = input("message: ")
        
        callback = False
        socket_server.send(f"{login}\n{login_to_client}\n{message}|".encode('utf-8'))

def receive_messages(socket_server:socket.socket):
    global authorized, callback
    
    while True:
        try:
            msg = socket_server.recv(1024).decode('utf-8')
            if msg.startswith("COMMAND:"):
                code = int(msg.split(":")[1])
                if code == SUCCES_AUTHORIZE:
                    authorized = True
                elif code == ERROR_SEND:
                    print("Error send message")
                    callback = True
                elif code == SUCCES_SEND:
                    callback = True
                
                continue
            
            print(msg)
        except:
            print("[!] Соединение потеряно.")
            break    
    
def start_client():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.connect((ip_host, port))
    
    print("[*] connect to server")
    
    chat_thread = threading.Thread(target=chat_activity, args=(socket_server, ))
    chat_thread.start()
    thread_list.append(chat_thread)
    
    receive_messages_thread = threading.Thread(target=receive_messages, args=(socket_server, ))
    receive_messages_thread.start()
    thread_list.append(receive_messages_thread)
    
    
    
if __name__ == "__main__":
    start_client()