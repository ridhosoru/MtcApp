import requests
import ast
import json

class registerModel:
    def registerS(self,username,password,email):
        url ="http://127.0.0.1:8000//registerAcc"
        payload = {"username":username, "password":password,"email":email}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return {"username":username, "password":password,"email":email} 
            else:
                if response.status_code == 409:
                    message = "username already used"
                    return False,message
                elif response.status_code == 400:
                    message = "email already used"
                    return False,message
                else :
                    message = "error check your internet,you email format etc"
        except Exception as e:
            print(e)

class LoginModel:
    def loginS(self,username,password):
        url ="http://127.0.0.1:8000//loginAcc"
        payload = {"username":username, "password":password}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return True,{"username":username, "password":password} 
            elif response.status_code == 500:
                message = "wrong username or password"
                return False,message
                
        except Exception as e:
            print(e)