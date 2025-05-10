import json
import os
from client_data import Client

SUCCES_AUTHORIZE = 101
ERROR_AUTHORIZE = 102

SUCCES_SEND = 201
ERROR_SEND = 202


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