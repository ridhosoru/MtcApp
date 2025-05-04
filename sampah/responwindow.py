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

class responWindow(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("responWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeW)
        self.updateTable()
        self.setupAutoRefresh()
        self.responseButton.clicked.connect(self.responsCalling)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    
    def responsCalling(self):
        selected_row = self.tableWidget.currentRow()
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            #rowdata['status'] = 'waiting'
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'waiting'
            rowdata['timeRs'] = datetime.now().strftime("%H:%M:%S")
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
                    print("success")
                    self.close()
                else :
                    print(response.status_code)
            except Exception as e:
                print(e)
                
    
    def updateTable(self):
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
        self.timerT.timeout.connect(self.updateTable)
        self.timerT.start(3000)


    def closeW(self):
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