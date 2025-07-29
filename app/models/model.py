import requests

class getConn :
    def get_conn():
        url ="http://103.179.56.80/"
        try :
            response = requests.get(url)
            if response.status_code == 200 :
                return response.json()
            else :
                return None
        except Exception as e :
            print(e)


class registerSModel:
    def registerS(self,username,password,email):
        url ="http://103.179.56.80/registerAcc"
        payload = {"username":username, "password":password,"email":email}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def adminacc(self):
        url = "http://103.179.56.80/getCred"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    email = data.get("email")
                    password = data.get("password")
                    return email, password
                except Exception as e:
                    print("JSON parse error:", e)
                    return None
            else:
                print("Gagal ambil kredensial")
                return None
        except requests.exceptions.RequestException as e:
            print("Network error:", e)
            return None


class LoginSModel:
    def loginS(self,username,password):
        url ="http://103.179.56.80/loginAcc"
        payload = {"username":username, "password":password}
        
        try :
            response = requests.post(url, json=payload)
            if response.status_code == 200 :
                return response.json()
            elif response.status_code == 500:
                message = "wrong username or password"
                return False,message
                
        except Exception as e:
            print(e)
                        

class loginmodel:
    def login(self,username,password,id):
        url ="http://103.179.56.80/loginUser"
        payload = {"username":username, "password":password, "id":id}
        
        try :
            response = requests.post(url, json=payload)
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
            url ="http://103.179.56.80//RegisterUser"
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
            url ="http://103.179.56.80/getTask"
            response = requests.get(url)
            if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
            print(e)
    
    def getStatusRespon(self):
        url= "http://103.179.56.80/getstatusR"
        try :
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                return result
        except Exception as e :
            return None
        
    def getMaintenanceP(self,dateSt,id):
        try:
            payload={
                "id" : id,
                "datestart": dateSt
            }
            url= "http://103.179.56.80/getTask"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
    
    def getAllTask(self,id):
        try:
            payload={
                "id" : id,
            }
            url= "http://103.179.56.80/getAllTask"
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
            url ="http://103.179.56.80/lineName"
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
            url ="http://103.179.56.80/machineName"
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
            url ="http://103.179.56.80/problemName"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                data = response.json()
            return data
        except Exception as e:
            print(e)
    
    def callmodel(self,id,locc,machinec,probc,commentText,dateSt,timeSt,timeRs,status,solve,problemafterc,timefinish,namemtc):
        try:
            url = "http://103.179.56.80/TaskInput"
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
            url= "http://103.179.56.80/getRespon"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
    
    def responseCModel(self,rowdata,id):
        try :
            url = "http://103.179.56.80/TaskUpdate"
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
            url= "http://103.179.56.80/getRespon"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
    
    def closeTaskModel(self,rowdata,id):
        try :
            url = "http://103.179.56.80/TaskFinish"
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
    def sendNote(self,username,id,subject,notetext,datenote):
        url ="http://103.179.56.80/addnote"
        payload = {"username":username, "id":id,"subject":subject,"notetext":notetext,"datenote":datenote}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def getnote(self,id,username):
        url = "http://103.179.56.80/getNote"
        payload = {"id":id, "username":username}
        
        try :
            response = requests.post(url,json=payload)
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

class Regprod :
    def machineInp(self,id,name):
        url ="http://103.179.56.80/regMachine"
        payload = { "id":id,"name":name,}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def LocInp(self,id,name):
        url ="http://103.179.56.80/regLoc"
        payload = { "id":id,"name":name,}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def probInp(self,id,name):
        url ="http://103.179.56.80/regProb"
        payload = { "id":id,"name":name,}
        
        try :
            response = requests.post(url, json=payload)
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

class store :
    def addstore(self,id,namePart,codePart,typePart,stockPart,imgPath):
        url ="http://103.179.56.80/addstore"
        payload = { "id":id,"namepart":namePart,"codepart":codePart,"typepart":typePart, "stockpart":stockPart, "imgpath":imgPath}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def getStore(self,id):
        url = "http://103.179.56.80/getStorePart"
        payload = { "id":id}
        
        try :
            response = requests.post(url, json=payload)
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
    
    def storeList(self,id,name,typepart,codepart,qty2,date,user,location,machine,status):
        url = "http://103.179.56.80/takestorelist"
        payload = { "id":id,"namepart":name,"codepart":codepart,"typepart":typepart,"stocktake":qty2,"date":date,"nameuser":user,"location":location,"machine":machine, "status":status}
        
        try :
            response = requests.post(url, json=payload)
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

    def takepart(self,id,name,codepart,qtot):
        url = "http://103.179.56.80/takestock"
        payload = { "id":id,"namepart":name,"codepart":codepart,"stockpart":qtot}
        
        try :
            response = requests.post(url, json=payload)
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

    def getAllStoreAct(self,id):
        try:
            payload={
                "id" : id,
            }
            url= "http://103.179.56.80/getStoreList"
            response = requests.post(url,json=payload)
            if response.status_code == 200 :
                result= response.json()
                return result
        except Exception as e :
            print(e)
