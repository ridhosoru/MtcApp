from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np

class mainWinC:
    def __init__(self,mainView,appcontext):
        self.mainView = mainView
        self.appcontextw = appcontext
        self.mainWindowController()
        
    def mainWindowController(self):
        self.mainWindowButtonController()
        self.timerU()
        self.tabletask()
        self.setupAutoRefresh()
        self.getStatusR()
        self.mtcPerfomance()
        
    def mtcPerfomance(self):
        self.getData()
        self.avgTimeRespon()
        self.totalTask()
        self.taskWaiting()
        self.taskComplete()
        self.avgTimeComplete()

    def getData(self):
        dateSt = str(datetime.now().strftime("%d-%m-%Y"))
        getData = MainModel.getMaintenanceP(self,dateSt)
        return getData
    
    def totalTask(self):
        getData = mainWinC.getData(self)
        if getData:
            status = [row[0] for row in getData]
            TotalTask = len(status)
            self.mainView.label_totTask.setText("TOTAL TASK : "+str(TotalTask))
    
    def taskWaiting(self):
        getData = mainWinC.getData(self)
        if getData :
            status = [row[0] for row in getData]
            tot_taskWaiting = status.count('waiting')
            self.mainView.label_taskWaiting.setText("TASK WAITING : "+str(tot_taskWaiting))
    
    def taskComplete(self):
        getData = mainWinC.getData(self)
        if getData :
            status = [row[0] for row in getData]
            tot_taskComplete = status.count('Done')
            self.mainView.label_taskComplete.setText("TASK COMPLETE:  "+str(tot_taskComplete))
    
    def avgTimeComplete(self):
        getData = mainWinC.getData(self)
        if getData:
            status = [row[0] for row in getData]
            timerespon = [row[3] for row in getData]
            timefinish = [row[10] for row in getData]
            formattime = '%H:%M:%S'
            if "Calling" in status:
                self.mainView.label_AvgTC.setText("AVG TIME COMPLETE : Complete Task Waiting")
            elif "waiting" in status :
                self.mainView.label_AvgTC.setText("AVG TIME COMPLETE : Complete Task Waiting")
            else :
                timefinishdt = [datetime.strptime(time,formattime)for time in timefinish]
                timerespondt = [datetime.strptime(time,formattime)for time in timerespon]
                timeoperate = [finish-respon for finish,respon in zip(timefinishdt,timerespondt)]
                total_seconds = sum(delta.total_seconds()for delta in timeoperate)
                totalminutes = total_seconds/60
                avgminutes= totalminutes/len(getData)
                if avgminutes >= 60 :
                    avghours = round(avgminutes/60,2)
                
                    self.mainView.label_AvgTC.setText("AVG TIME COMPLETE(Hours) : "+str(avghours))
                else:
                    avgminutes_up= round(avgminutes,2)
                    self.mainView.label_AvgTC.setText("AVG TIME COMPLETE(minutes) : "+str(avgminutes_up))


            
    def avgTimeRespon(self):
        getData = mainWinC.getData(self)
        if getData:
            timerespon = [row[3] for row in getData]
            timestart = [row[2] for row in getData]
            status = [row[0] for row in getData]
            formattime = '%H:%M:%S'
            if "Calling" in status :
                if '-' in timerespon:
                    self.mainView.label_avgTR.setText("AVG TIME RESPON(Hours) : Respon Another Call")
            else:
                timestartdt = [datetime.strptime(time,formattime)for time in timestart]
                timerespondt = [datetime.strptime(time,formattime)for time in timerespon]
                timeoperate = [respon-start for start,respon in zip(timestartdt,timerespondt)]
                total_seconds = sum(delta.total_seconds()for delta in timeoperate)
                totalminutes = total_seconds/60
                avgminutes= totalminutes/len(getData)
                if avgminutes >= 60 :
                    avghours = round(avgminutes/60,2)
                
                    self.mainView.label_avgTR.setText("AVG TIME RESPON(Hours) : "+str(avghours))
                else:
                    avgminutes_up= round(avgminutes,2)
                    self.mainView.label_avgTR.setText("AVG TIME RESPON(minutes) : "+str(avgminutes_up))
    
    def getStatusR(self):
        modelRespon = mainWinC.getData(self)
        if modelRespon :
            status = [row[0] for row in modelRespon]
            if "Calling" in status:
                self.mainView.callresponseButton.setStyleSheet("background-color: yellow;")
            elif "waiting" in status:
                self.mainView.closecallButton.setStyleSheet("background-color: yellow;")
            else:
                self.mainView.callresponseButton.setStyleSheet("")
                self.mainView.closecallButton.setStyleSheet("")


    def mainWindowButtonController(self):
        self.mainView.callButton.clicked.connect(self.callButtonA)
        self.mainView.callresponseButton.clicked.connect(self.responseButtonA)
        self.mainView.closecallButton.clicked.connect(self.closeCallA)
    
    def closeCallA(self):
        self.appcontextw.closeCallWindow()
    
    def responseButtonA(self):
        self.appcontextw.responseWindow()

    def callButtonA(self):
        self.appcontextw.callWindow()        

    def tabletask(self):
        dateSt = str(datetime.now().strftime("%d-%m-%Y"))
        # getData = MainModel.getMaintenanceP(self,dateSt)
        tabletaskupdate= MainModel.getMaintenanceP(self,dateSt)
        status_order = ['Calling', 'waiting', 'Done']
        tabletaskupdate.sort(key=lambda row: status_order.index(row[0]) if row[0] in status_order else len(status_order))
        # tabletaskupdate = MainModel.tableTaskM(self)
        if tabletaskupdate :
            self.mainView.tableWidget.setRowCount(len(tabletaskupdate))
            for row_idx, row in enumerate(tabletaskupdate):
                for col_idx, value in enumerate(row):
                    self.mainView.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        for i in range(7, 10):
            self.mainView.tableWidget.setColumnWidth(i, 250)

    def timerU(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(1000)
        
    
    def updateDate(self):
        nowDate = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.mainView.dateLabel.setText(nowDate)

    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.tabletask)
        self.timerT.timeout.connect(self.getStatusR)
        self.timerT.timeout.connect(self.mtcPerfomance)
        self.timerT.start(5000)




        



    

        







        

        