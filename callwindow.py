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


class callWindow(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("callWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeCall)
        #########
        self.lineList()
        self.machineList()
        self.probList()
        self.okCallButton.clicked.connect(self.okCall)

    def lineList(self):
        try:
             url ="http://127.0.0.1:8000/dataLine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                self.loccomboBox.addItems(data)
        except Exception as e:
                print(e)
    
    def machineList(self):
        try:
             url ="http://127.0.0.1:8000/dataMachine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                self.machinecomboBox.addItems(data)
        except Exception as e:
                print(e)
    
    def probList(self):
        try:
            url ="http://127.0.0.1:8000/dataProblem"
            response = requests.get(url)
            if response.status_code == 200 :
               data = response.json()
               self.probcomboBox.addItems(data)
        except Exception as e:
            print(e)

    def okCall(self):
        locc=self.loccomboBox.currentText()
        machinec=self.machinecomboBox.currentText()
        probc=self.probcomboBox.currentText()
        commentText=self.commentTextEdit.toPlainText()
        dateSt = datetime.now().strftime("%d-%m-%Y")
        timeSt = datetime.now().strftime("%H:%M:%S")
        timeRs = "-"
        status = "Calling"
        solve = "-"
        problemafterc="-"
        timefinish="-"
        namemtc="-"
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
                print("success")
                self.close()
            else :
                print(response.status_code)
        except Exception as e:
            print(e)

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
