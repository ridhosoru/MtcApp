import requests

class loginmodel:
    def login(self,username,password):
        url ="http://127.0.0.1:8000/login"
        payload = {"username":username, "password":password}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return {"username":username, "password":password}
            else:
                return None
        except Exception as e:
            print(e)

class registermodel:
    def register(self,username,password):
        try :
            url ="http://127.0.0.1:8000/register"
            payload = {"username": username, "password": password}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json
            else :
                return None
        except Exception as e:
            print(e)

class MainModel:
    def tableTaskM(self):
        try:
            url ="http://127.0.0.1:8000/getTask"
            response = requests.get(url)
            if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
            print(e)

class callWModel:
    def linemodel(self):
        try:
             url ="http://127.0.0.1:8000/dataLine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
                print(e)
    
    def machinemodel(self):
        try:
             url ="http://127.0.0.1:8000/dataMachine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
            print(e)
    
    def probmodel(self):
        try:
            url ="http://127.0.0.1:8000/dataProblem"
            response = requests.get(url)
            if response.status_code == 200 :
               data = response.json()
               return data
        except Exception as e:
            print(e)
                                    