from client_data import Client

class Authorize_servis:
    def __init__(self, authorize_data:dict[str,Client]):
        self.__authorize_data = authorize_data
    
    def check_client_login_and_password(self, login:str, password:str) -> bool:
        return login in self.__authorize_data and self.__authorize_data[login].password == password