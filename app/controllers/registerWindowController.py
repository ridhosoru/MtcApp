from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np

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
        if username and password :
            registeru = registermodel()
            registerdata = registeru.register(username,password)
            if registerdata :
                QMessageBox.information(self.registerw,"success","success add user")
                self.registerw.usernameLine.clear()
                self.registerw.passwordLine.clear()
            else:
                QMessageBox.warning(self.registerw,"Fail","username already used")
        else :
            QMessageBox.warning(self.registerw,"Fail","Fill in username or password")