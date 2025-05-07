from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np

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
            rowdata['namemtc'] = self.appcontextw.getuser
            postCloseTask = closeCModel.closeTaskModel(self,rowdata)
            if postCloseTask :
                self.closeV.close()
    
    def updateTableC(self):
        updateTable = closeCModel.updatetable(self)
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