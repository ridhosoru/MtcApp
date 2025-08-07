from models.model import loginmodel
from PyQt6.QtWidgets import QMessageBox
import os
import  json
from pathlib import Path

class logincontroller:
    def __init__(self,loginv,appcontext):
        self.loginv = loginv
        self.appcontextw = appcontext
        self.logincontroll()
    
    def logincontroll(self):
        self.loginv.loginButton.clicked.connect(self.logincontrolBtn)
        self.loginv.registerButton.clicked.connect(self.registerBtn)
        self.loginv.closeButton.clicked.connect(self.closeLogin)
        self.loginv.logoutBtn.clicked.connect(self.logout)

    def logout(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        session_path = appdata_dir / "session.json"
        if session_path.exists():
            os.remove(session_path)
            self.loginv.close()
            self.appcontextw.openStarted()
    
    def closeLogin(self):
        self.loginv.close()
    
    def getID(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        session_path = appdata_dir / "session.json"
        if session_path.exists():
            with open(session_path, "r") as f:
                data = json.load(f)
                return data.get("id")

    def logincontrolBtn(self):
        username = self.loginv.usernameLine.text()
        password = self.loginv.passwordLine.text()
        id = int(self.getID())
        
        try:
            if username and password :
                logincheck = loginmodel()
                logindata = logincheck.login(username,password,id)
                if logindata:
                    data = logindata[0]
                    getUsername = data['username']
                    getid = data['id']
                    worknumber = data['worknumber']
                    self.saveLogInfo(getid,getUsername,worknumber)
                    self.appcontextw.openmainWindow()
                    self.loginv.close()
                else :
                    QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
            else :
                QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
        except Exception as e:
            QMessageBox.warning(self.loginv,"fail",str(e))

    def saveLogInfo(self,getid,getUsername,worknumber):
        session_data = {"id":getid,"username": getUsername,"worknumber":worknumber}
        save_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        save_dir.mkdir(parents=True, exist_ok=True)
        json_path = save_dir / "user.json"
        with open(json_path, "w") as f:
            json.dump(session_data, f)
    
    def registerBtn(self):
        self.appcontextw.openregisterWindow()
        self.loginv.close()