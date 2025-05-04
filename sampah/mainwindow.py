import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import Qt,QPoint, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import requests
from datetime import datetime
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import pyqtSignal

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
        self.callButton.setIcon(QIcon("icon/call.png"))
        self.callButton.setIconSize(QSize(32, 32))
        self.tableTask()
        self.setupAutoRefresh()
        self.callresponseButton.clicked.connect(self.callRespon)
        self.callresponseButton.setIcon(QIcon("icon/respon.png"))
        self.callresponseButton.setIconSize(QSize(32, 32))
        self.statusResponseC()
        self.closecallButton.clicked.connect(self.closerespon)
        self.closecallButton.setIcon(QIcon("icon/classcall.png"))
        self.closecallButton.setIconSize(QSize(32, 32))
        
        # self.setupAutoRefreshrS()
    
    def closerespon(self):
        self.closeR = closeresponWindow(self.usernameLogin)
        self.closeR.show()

    def statusResponseC(self):
        try:
            url= "http://127.0.0.1:8000/getstatusR"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                data_list = result.get("data", [])
                if "Calling" in data_list:
                    self.callresponseButton.setStyleSheet("background-color: red;")
                elif "waiting" in data_list:
                    self.callresponseButton.setStyleSheet("background-color: yellow;")
                else :
                    self.callresponseButton.setStyleSheet("")

        except Exception as e:
            print(e)  

    def callRespon(self,):
        self.responw = responWindow()
        self.responw.show()

    
    def tableTask(self):
        try:
            url ="http://127.0.0.1:8000/getTask"
            response = requests.get(url)
            if response.status_code == 200 :
               data = response.json()
               if data :
                   self.tableWidget.setRowCount(len(data))
                   for row_idx, row in enumerate(data):
                       for col_idx, value in enumerate(row):
                           self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            for i in range(7, 10):
                self.tableWidget.setColumnWidth(i, 250)

        except Exception as e:
            print(e)

    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.tableTask)
        self.timerT.timeout.connect(self.statusResponseC)
        self.timerT.start(3000)

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
