import requests




class registerSModel:
    def registerS(self,username,password,email):
        url ="http://127.0.0.1:8000/registerAcc"
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


class LoginSModel:
    def loginS(self,username,password):
        url ="http://127.0.0.1:8000/loginAcc"
        payload = {"username":username, "password":password}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return response.json()
            elif response.status_code == 500:
                message = "wrong username or password"
                return False,message
                
        except Exception as e:
            print(e)
                        

class loginmodel:
    def login(self,username,password,id):
        url ="http://127.0.0.1:8000/loginUser"
        payload = {"username":username, "password":password, "id":id}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                return response.json()
            elif response.status_code == 409:
                return None  
            else:
                return None 
        except Exception as e:
            print(e)

class registermodel:
    def register(self,username,password,workNumber,id):
        try :
            url ="http://127.0.0.1:8000//RegisterUser"
            payload = {"username": username, "password": password, "workNumber":workNumber, "id":id}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
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
    
    def getStatusRespon(self):
        url= "http://127.0.0.1:8000/getstatusR"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            return result
        
    def getMaintenanceP(self,dateSt,id):
        try:
            payload={
                "id" : id,
                "datestart": dateSt
            }
            url= "http://127.0.0.1:8000/getTask"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
            
class callWModel:
    def linemodel(self,id):
        try:
            payload={
                "id": id
            }
            url ="http://127.0.0.1:8000/lineName"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                data = response.json()
            return data
        except Exception as e:
            print(e)
    
    def machinemodel(self,id):
        try:
            payload={
                "id": id
            }
            url ="http://127.0.0.1:8000/machineName"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                data = response.json()
            return data
        except Exception as e:
            print(e)
    
    def probmodel(self,id):
        try:
            payload={
                "id": id
            }
            url ="http://127.0.0.1:8000/issueTable"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                data = response.json()
            return data
        except Exception as e:
            print(e)
    
    def callmodel(self,id,locc,machinec,probc,commentText,dateSt,timeSt,timeRs,status,solve,problemafterc,timefinish,namemtc):
        try:
            url = "http://127.0.0.1:8000/TaskInput"
            payload = { "id"    : id,
                        "status": status, 
                        "datestart": dateSt,
                        "timestart": timeSt,
                        "timerespon": timeRs,
                        "location": locc,
                        "machine": machinec,
                        "problem": probc,
                        "commenttxt": commentText,
                        "problemaftercheck": problemafterc,
                        "solve": solve,
                        "timefinish": timefinish,
                        "namemtc": namemtc}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
            else :
                print(response.status_code)
        except Exception as e:
            print(e) 

class responModel:
    def tableModel(self,dateSt,id):
        try:
            payload={
                "id" :id,
                "datestart": dateSt,
                "status":'Calling'
            }
            url= "http://127.0.0.1:8000/getRespon"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
    
    def responseCModel(self,rowdata,id):
        try :
            url = "http://127.0.0.1:8000/TaskUpdate"
            payload = {
                        "id":id,
                        "status": rowdata['status'],
                        "datestart": rowdata['dateSt'],
                        "timestart": rowdata['timeSt'],
                        "timerespon": rowdata['timeRs'],
                        "commenttxt": rowdata['commentText'],
                        }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data=response.json()
                return data
            else :
                print(response.status_code)
        except Exception as e:
            print(e)

class closeCModel:
    def tableModel(self,dateSt,id):
        try:
            payload={
                "id" :id,
                "datestart": dateSt,
                "status":'waiting'
            }
            url= "http://127.0.0.1:8000/getRespon"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
    
    def closeTaskModel(self,rowdata,id):
        try :
            url = "http://127.0.0.1:8000/TaskFinish"
            payload = {"id":id,
                        "status": rowdata['status'],
                        "datestart": rowdata['dateSt'],
                        "timestart": rowdata['timeSt'],
                        "timerespon": rowdata['timeRs'],
                        "commenttxt": rowdata['commentText'],
                        "problemaftercheck": rowdata['problemafterc'],
                        "solve": rowdata['solve'],
                        "timefinish": rowdata['timefinish'],
                        "namemtc": rowdata['namemtc']}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data
            else :
                print(response.status_code)
        except Exception as e:
                print(e)

class addNote:
    def sendNote(self,username,id,subject,notetext):
        url ="http://127.0.0.1:8000/addnote"
        payload = {"username":username, "id":id,"subject":subject,"notetext":notetext}
        response = requests.post(url, json=payload)
        try :
            if response.status_code == 200 :
                data=response.json()
                return data
            else:
                if response.status_code == 409:
                    message = "error"
                    return False,message
                else :
                    message = "error"
        except Exception as e:
            print(e)