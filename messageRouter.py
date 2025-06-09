from client_data import Client
from decorators import overload_by_arg_count

class MessageRouter:
    def __init__(self, authorize_data:dict[str,Client]):
        self.__authorize_data = authorize_data
    
    @overload_by_arg_count()
    def route(self): raise SyntaxError("Use one is overloads")
    
    @overload_by_arg_count.register(2)
    def route(self, to_client:Client, message:str):
        if to_client.login not in self.__authorize_data:
            print(f"[error] client {to_client.login} not found in client data")
            return
        
        to_client.socket_client.send(f"{message}".encode())
        
    @overload_by_arg_count.register(3)
    def route(self, from_client:Client, to_client:Client, message:str):
        if from_client.login not in self.__authorize_data:
            print(f"[error] client {from_client.login} not found in client data")
            return
        
        if to_client.login not in self.__authorize_data:
            print(f"[error] client {to_client.login} not found in client data")
            return
        
        to_client.socket_client.send(f"{from_client.login}: {message}".encode())
        