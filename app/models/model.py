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
    
    def callmodel(self,locc,machinec,probc,commentText,dateSt,timeSt,timeRs,status,solve,problemafterc,timefinish,namemtc):
        try:
            url = "http://127.0.0.1:8000/taskInput"
            payload = {"status": status, 
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
    def tableModel(self):
        try:
            url ="http://127.0.0.1:8000/getTask"
            response = requests.get(url)
            if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
            print(e)
    
    def responseCModel(self,rowdata):
        try :
            url = "http://127.0.0.1:8000/updaterespon"
            payload = {"status": rowdata['status'],
                        "datestart": rowdata['dateSt'],
                        "timestart": rowdata['timeSt'],
                        "timerespon": rowdata['timeRs'],
                        "location": rowdata['locc'],
                        "machine": rowdata['machinec'],
                        "problem": rowdata['probc'],
                        "commenttxt": rowdata['commentText'],
                        "problemaftercheck": rowdata['problemafterc'],
                        "solve": rowdata['solve'],
                        "timefinish": rowdata['timefinish'],
                        "namemtc": rowdata['namemtc']}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data=response.json()
                return data
            else :
                print(response.status_code)
        except Exception as e:
            print(e)

class closeCModel:
    def updatetable(self):
        try:
            url ="http://127.0.0.1:8000/getTask"
            response = requests.get(url)
            if response.status_code == 200 :
                data = response.json()
                return data
        except Exception as e:
            print(e)
    
    def closeTaskModel(self,rowdata):
        try :
            url = "http://127.0.0.1:8000/closetask"
            payload = {"status": rowdata['status'],
                        "datestart": rowdata['dateSt'],
                        "timestart": rowdata['timeSt'],
                        "timerespon": rowdata['timeRs'],
                        "location": rowdata['locc'],
                        "machine": rowdata['machinec'],
                        "problem": rowdata['probc'],
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

                                    