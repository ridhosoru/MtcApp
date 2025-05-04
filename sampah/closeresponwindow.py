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

class closeresponWindow(QtWidgets.QMainWindow):
    def __init__(self,usernameLogin,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("responclosewindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeW)
        self.updateTable()
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.closetaskButton.clicked.connect(self.closetask)
        self.usernameLogin= usernameLogin

    
    def closetask(self):
        selected_row = self.tableWidget.currentRow()
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'Done'
            rowdata['problemafterc'] = self.probactext.toPlainText()
            rowdata['solve'] = self.solvetext.toPlainText()
            rowdata['timefinish'] = datetime.now().strftime("%H:%M:%S")
            rowdata['namemtc'] = self.usernameLogin
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
                print(payload)
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