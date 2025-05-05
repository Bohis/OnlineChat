import typing
import socket

class Client:
    def __init__(self, login:str, password:str):
        self.__login = login
        self.__password = password
        self.__ip = None
        self.__socket_client = None
    
    @property
    def login(self) -> str: return self.__login
    
    @property
    def password(self) -> str: return self.__password

    @property
    def ip(self) -> str: return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value
        
    @property
    def socket_client(self) -> socket.socket: return self.__socket_client
    
    @socket_client.setter
    def socket_client(self, other: socket.socket):
        self.__socket_client = other 
    
    def __eq__(self, other: typing.Self) -> bool:
        if type(other) != Client:
            return False
        
        return self.login == other.login and self.password == other.password
    
    def __str__(self) -> str:
        return f"login:{self.__login}\npassword:{self.__password}"
    
    def __repr__(self) -> str:
        return f"\"{self.__login}, {self.__password}\""

    

if __name__ == "__main__":
    client1 = Client("test_login", "test_password")
    client2 = Client("test_login", "test_password")
    client3 = Client("test_login14", "test_password")
    client4 = Client("test_login", "test_password12")
    client5 = Client("test_logi12n", "test_password12")
    
    print(client1)
    print(client2)
    print(client1 == client2)
    print(client1 == client3)
    print(client2 == client4)
    print(client1 == client5)
        