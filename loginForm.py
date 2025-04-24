import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import Qt,QPoint, QTimer
from PyQt6.QtWidgets import QMessageBox
import requests
from datetime import datetime

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("login.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.closeButton.clicked.connect(self.closeApp)
        self.loginButton.clicked.connect(self.loginApp)
        self.registerButton.clicked.connect(self.registerW)

    def loginApp(self):
        usernameLogin = self.usernameLine.text()
        password = self.passwordLine.text()

        if usernameLogin or password :
            try:
                url ="http://127.0.0.1:8000/login"
                payload = {"username": usernameLogin, "password": password}
                response = requests.post(url, json=payload)
                if response.status_code == 200 :
                    print("login success")
                    QMessageBox.information(self,"Success","Login Success")
                    self.mains = mainshow(usernameLogin)
                    self.mains.show()
                    self.close()
                else:
                    QMessageBox.warning(self,"Fail","wrong username or password")
            except Exception as e :
                QMessageBox.warning(self,"Fail",e)
        else:
            QMessageBox.warning(self,"Fail","Fill in username or password")
    
    def closeApp(self):
        closenotif = QMessageBox.question(self, 'Close Application', 'are you sure to close application?', QMessageBox.StandardButton.No| QMessageBox.StandardButton.Yes)
        if closenotif == QMessageBox.StandardButton.Yes:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def registerW(self):
        self.reg = registerWindow()
        window.close()
        self.reg.show()

###################################
class registerWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("registerUser.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.backButton.clicked.connect(self.back2Log)
        self.registerButton.clicked.connect(self.regUser)
    
    def regUser(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        if username or password :
            try:
                url ="http://127.0.0.1:8000/register"
                payload = {"username": username, "password": password}
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    QMessageBox.information(self,"success","success add user")
                    self.usernameLine.clear()
                    self.passwordLine.clear()
                else :
                    QMessageBox.warning(self,"Fail","username already used")
            except Exception as e:
                QMessageBox.warning(self,"Fail",e)
        else:
            QMessageBox.warning(self,"Fail","Fill in username or password")

    def back2Log(self):
        window.show()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

#########################################################
class mainshow(QtWidgets.QMainWindow):
    def __init__(self, usernameLogin,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        #timerdate
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(1000)
        self.usernameLogin= usernameLogin
        self.userLabel.setText("Hi, "+ self.usernameLogin)
        self.callButton.clicked.connect(self.call)
    
    def call(self):
        self.callw = callWindow()
        self.callw.show()

    def updateDate(self):
        nowDate = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.dateLabel.setText(nowDate)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
####
class callWindow(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("callWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeCall)
    
    def closeCall(self):
        self.close()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()