import requests

class loginmodel:
    def login(self,username,password):
        url ="http://127.0.0.1:8000/login"
        payload = {"username":username, "password":password}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return response.json
            else:
                return None
        except Exception as e:
            print(e)

class registermodel:
    def register(self,username,password):
        url ="http://127.0.0.1:8000/register"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json
        else :
            return None
                
    
                                    