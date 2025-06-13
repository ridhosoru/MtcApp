from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import os
import  json

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
        if os.path.exists("session.json"):
            os.remove("session.json")
            self.loginv.close()
            self.appcontextw.openStarted()
    
    def closeLogin(self):
        self.loginv.close()
    
    def getID(self):
        if os.path.exists("session.json"):
            with open("session.json", "r") as f:
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
            print(e)

    def saveLogInfo(self,getid,getUsername,worknumber):
        session_data = {"id":getid,"username": getUsername,"worknumber":worknumber}
        with open("user.json", "w") as f:
            json.dump(session_data, f)
    
    def registerBtn(self):
        self.appcontextw.openregisterWindow()
        self.loginv.close()