from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import os,json


class callWindowController:
    def __init__(self,callWindowView,appcontext):
        self.callWindowView = callWindowView
        self.appcontextw = appcontext
        self.callController()
        self.machineList()
    
    def callController(self):
        self.callControllerButton()
        self.lineList()
        self.machineList()
        self.problist()
    
    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")

    
    def lineList(self):
        id = int(self.getID())
        linegetm = callWModel.linemodel(self,id)
        if linegetm :
            name_list = [item['name'] for item in linegetm]
            self.callWindowView.loccomboBox.clear()
            self.callWindowView.loccomboBox.addItems(name_list)

    def machineList(self):
        id = int(self.getID())
        machinegetm = callWModel.machinemodel(self,id)
        if machinegetm :
            name_list = [item['name'] for item in machinegetm]
            self.callWindowView.machinecomboBox.clear()
            self.callWindowView.machinecomboBox.addItems(name_list)

    def problist(self):
        id = int(self.getID())
        probgetm = callWModel.probmodel(self,id)
        if probgetm :
               name_list = [item['issue'] for item in probgetm]
               self.callWindowView.probcomboBox.clear()
               self.callWindowView.probcomboBox.addItems(name_list)
    
    def callControllerButton(self):
        self.callWindowView.cancelButton.clicked.connect(self.closeCall)
        self.callWindowView.okCallButton.clicked.connect(self.okCall)
    
    def okCall(self):
        id = int(self.getID())
        locc=self.callWindowView.loccomboBox.currentText()
        machinec=self.callWindowView.machinecomboBox.currentText()
        probc=self.callWindowView.probcomboBox.currentText()
        commentText=self.callWindowView.commentTextEdit.toPlainText()
        dateSt = datetime.now().strftime("%d-%m-%Y")
        timeSt = datetime.now().strftime("%H:%M:%S")
        timeRs = "-"
        status = "Calling"
        solve = "-"
        problemafterc="-"
        timefinish="-"
        namemtc="-"
        callmodel= callWModel.callmodel(self,id,locc,machinec,probc,commentText,dateSt,timeSt,timeRs,status,solve,problemafterc,timefinish,namemtc)
        if callmodel:
            self.appcontextw.openmainWindow()
            self.callWindowView.close()

    def closeCall(self):
        self.callWindowView.close()