from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import json
import os

class registerwindowcontroller:
    def __init__(self,registerw,appcontext):
        self.registerw = registerw
        self.appcontextw = appcontext
        self.registercontroll()
    
    def registercontroll(self):
        self.registerw.backButton.clicked.connect(self.back2log)
        self.registerw.registerButton.clicked.connect(self.registerU)

    def back2log(self):
        self.appcontextw.open_loginwindow()
        self.registerw.close()
    
    def registerU(self):
        username = self.registerw.usernameLine.text()
        password = self.registerw.passwordLine.text()
        workNumber = self.registerw.workNumberLine.text()
        id = self.getID()
        if username and password :
            registeru = registermodel()
            registerdata = registeru.register(username,password,workNumber,id)
            if registerdata :
                QMessageBox.information(self.registerw,"success","success add user")
                self.registerw.usernameLine.clear()
                self.registerw.passwordLine.clear()
                self.registerw.workNumberLine.clear()
            else:
                QMessageBox.warning(self.registerw,"Fail","username already used")
        else :
            QMessageBox.warning(self.registerw,"Fail","Fill in username or password")
    
    def getID(self):
        if os.path.exists("session.json"):
            with open("session.json", "r") as f:
                data = json.load(f)
                return data.get("id")