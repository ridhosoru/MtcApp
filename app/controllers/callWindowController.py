from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np


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
    
    def lineList(self):
        linegetm = callWModel.linemodel(self)
        if linegetm :
            self.callWindowView.loccomboBox.addItems(linegetm)

    def machineList(self):
        machinegetm = callWModel.machinemodel(self)
        if machinegetm :
               self.callWindowView.machinecomboBox.addItems(machinegetm)

    def problist(self):
        probgetm = callWModel.probmodel(self)
        if probgetm :
               self.callWindowView.probcomboBox.addItems(probgetm)
    
    def callControllerButton(self):
        self.callWindowView.cancelButton.clicked.connect(self.closeCall)
        self.callWindowView.okCallButton.clicked.connect(self.okCall)
    
    def okCall(self):
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
        callmodel= callWModel.callmodel(self,locc,machinec,probc,commentText,dateSt,timeSt,timeRs,status,solve,problemafterc,timefinish,namemtc)
        if callmodel:
            self.appcontextw.openmainWindow(self.appcontextw.getuser)
            self.callWindowView.close()

    def closeCall(self):
        self.callWindowView.close()