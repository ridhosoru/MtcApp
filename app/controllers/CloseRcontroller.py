from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import os, json

class closeRcontroller:
    def __init__(self,closeV,appcontext):
        self.closeV = closeV
        self.appcontextw = appcontext
        self.closeRcontroller()
    
    def closeRcontroller(self):
        self.closeRButtonController()
        self.updateTableC()
        self.setupAutoRefresh()
    
    def closeRButtonController(self):
        self.closeV.cancelButton.clicked.connect(self.closeVw)
        self.closeV.closetaskButton.clicked.connect(self.closeTask)
    
    def closeTask(self):
        selected_row = self.closeV.tableWidget.currentRow()
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            for col in range(self.closeV.tableWidget.columnCount()):
                item = self.closeV.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'Done'
            rowdata['problemafterc'] = self.closeV.probactext.toPlainText()
            rowdata['solve'] = self.closeV.solvetext.toPlainText()
            rowdata['timefinish'] = datetime.now().strftime("%H:%M:%S")
            rowdata['namemtc'] = self.getUsername()
            id = self.getID()
            postCloseTask = closeCModel.closeTaskModel(self,rowdata,id)
            if postCloseTask :
                self.closeV.close()
    
    def getUsername(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("username") 
    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")  
            
    def getData(self):
        dateSt = str(datetime.now().strftime("%d-%m-%Y"))
        id = self.getID()
        getData = closeCModel.tableModel(self,dateSt,id)
        if not getData or not isinstance(getData[0], dict):
            self.array_respon = []
            return self.array_respon
        name_list = [item['status'] for item in getData]
        print(name_list)
        if 'waiting' in name_list:
            self.array_respon = [list(item.values())[1:] for item in getData]
        else:
            self.array_respon=[]
        return self.array_respon
    
    def updateTableC(self):
        updateTable = self.getData()
        print(updateTable)
        if updateTable:
            self.closeV.tableWidget.setRowCount(len(updateTable))
            for row_idx, row in enumerate(updateTable):
                for col_idx, value in enumerate(row):
                    self.closeV.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        for i in range(7, 10):
            self.closeV.tableWidget.setColumnWidth(i, 250)
    
    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.updateTableC)
        self.timerT.start(3000)

    
    def closeVw (self):
        self.closeV.close()