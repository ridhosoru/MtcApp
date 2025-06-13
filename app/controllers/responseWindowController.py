from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import os,json
class responseWindowController:
    def __init__(self,responView,appcontext):
        self.responView = responView
        self.appcontextw = appcontext
        self.responseController()
    
    def responseController(self):
        self.responseControllerButton()
        self.updateTable()
        self.setupAutoRefresh()
        
    def responseControllerButton(self):
        self.responView.cancelButton.clicked.connect(self.closeR)
        self.responView.responseButton.clicked.connect(self.responsCalling)

    def responsCalling(self):
        selected_row = self.responView.tableWidget.currentRow()
        id = self.getID()
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            #rowdata['status'] = 'waiting'
            for col in range(self.responView.tableWidget.columnCount()):
                item = self.responView.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'waiting'
            rowdata['timeRs'] = datetime.now().strftime("%H:%M:%S")
            postResModel = responModel.responseCModel(self,rowdata,id)
            if postResModel :
                self.responView.close()
                self.appcontextw.openmainWindow()
    
    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")  
            
    def getData(self):
        dateSt = str(datetime.now().strftime("%d-%m-%Y"))
        id = self.getID()
        getData = responModel.tableModel(self,dateSt,id)
        if not getData or not isinstance(getData[0], dict):
            self.array_respon = []
            return self.array_respon
        name_list = [item['status'] for item in getData]
        print(name_list)
        if 'Calling' in name_list:
            self.array_respon = [list(item.values())[1:] for item in getData]
        else:
            self.array_respon=[]
        return self.array_respon

    def updateTable(self):
        gettableM = self.getData()
        if gettableM:
            self.responView.tableWidget.setRowCount(len(gettableM))
            for row_idx, row in enumerate(gettableM):
                for col_idx, value in enumerate(row):
                    self.responView.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        for i in range(7, 10):
            self.responView.tableWidget.setColumnWidth(i, 250)
    
    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.updateTable)
        self.timerT.start(3000)
    
    def closeR(self):
        self.responView.close()