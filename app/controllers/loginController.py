from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np

class logincontroller:
    def __init__(self,loginv,appcontext):
        self.loginv = loginv
        self.appcontextw = appcontext
        self.logincontroll()
    
    def logincontroll(self):
        self.loginv.loginButton.clicked.connect(self.logincontrolBtn)
        self.loginv.registerButton.clicked.connect(self.registerBtn)
        self.loginv.closeButton.clicked.connect(self.closeLogin)
    
    def closeLogin(self):
        self.loginv.close()

    def logincontrolBtn(self):
        username = self.loginv.usernameLine.text()
        password = self.loginv.passwordLine.text()
        try:
            if username and password :
                logincheck = loginmodel()
                logindata = logincheck.login(username,password)
                if logindata:
                    getUsername = logindata["username"]
                    self.appcontextw.getuser= getUsername
                    self.appcontextw.openmainWindow(getUsername)
                    self.loginv.close()
                else :
                    QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
            else :
                QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
        except Exception as e:
            print(e)
    
    def registerBtn(self):
        self.appcontextw.openregisterWindow()
        self.loginv.close()