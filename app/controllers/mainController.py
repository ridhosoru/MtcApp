from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel,addNote
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import numpy as np
import os,json
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
    #     # self.getStatusR()
        self.mtcPerfomance()
        self.getNote()
        self.allTask()
        
    def mtcPerfomance(self):
        self.avgTimeRespon()
        self.totalTask()
        self.taskWaiting()
        self.taskComplete()
        self.avgTimeComplete()
        self.getStatusR()
    
    def totalTask(self):
        if self.array_item:
            status = [row[0] for row in self.array_item]
            TotalTask = len(status)
            self.mainView.label_totTask.setText("TOTAL TASK : "+str(TotalTask))
    
    def taskWaiting(self):
        if self.array_item :
            status = [row[0] for row in self.array_item]
            tot_taskWaiting = status.count('waiting')
            self.mainView.label_taskWaiting.setText("TASK WAITING : "+str(tot_taskWaiting))
    
    def taskComplete(self):
        if self.array_item :
            status = [row[0] for row in self.array_item]
            tot_taskComplete = status.count('Done')
            self.mainView.label_taskComplete.setText("TASK COMPLETE:  "+str(tot_taskComplete))
    
    def avgTimeComplete(self):
        if self.array_item:
            status = [row[0] for row in self.array_item]
            timerespon = [row[3] for row in self.array_item]
            timefinish = [row[10] for row in self.array_item]
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
                avgminutes= totalminutes/len(self.array_item)
                if avgminutes >= 60 :
                    avghours = round(avgminutes/60,2)
                
                    self.mainView.label_AvgTC.setText("AVG TIME COMPLETE(Hours) : "+str(avghours))
                else:
                    avgminutes_up= round(avgminutes,2)
                    self.mainView.label_AvgTC.setText("AVG TIME COMPLETE(minutes) : "+str(avgminutes_up))


            
    def avgTimeRespon(self):
        if self.array_item:
            timerespon = [row[3] for row in self.array_item]
            timestart = [row[2] for row in self.array_item]
            status = [row[0] for row in self.array_item]
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
                avgminutes= totalminutes/len(self.array_item)
                if avgminutes >= 60 :
                    avghours = round(avgminutes/60,2)
                
                    self.mainView.label_avgTR.setText("AVG TIME RESPON(Hours) : "+str(avghours))
                else:
                    avgminutes_up= round(avgminutes,2)
                    self.mainView.label_avgTR.setText("AVG TIME RESPON(minutes) : "+str(avgminutes_up))
    
    def getStatusR(self):
        if self.array_item:
            status = [row[0] for row in self.array_item]
            
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
        self.mainView.closeButton.clicked.connect(self.closeM)
        self.mainView.minButton.clicked.connect(self.minM)
        self.mainView.logoutButton.clicked.connect(self.logout)
        self.mainView.addNButton.clicked.connect(self.openAddN)
    
    def openAddN(self):
        self.appcontextw.openNote()
        
    def logout(self):
        if os.path.exists("user.json"):
            os.remove("user.json")
            self.mainView.close()
            self.appcontextw.open_loginwindow()
    
    def minM(self):
        self.mainView.showMinimized()

    def closeM(self):
        self.mainView.close()
    
    def closeCallA(self):
        self.appcontextw.closeCallWindow()
    
    def responseButtonA(self):
        self.appcontextw.responseWindow()

    def callButtonA(self):
        self.appcontextw.callWindow()    

    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")  

    def tabletask(self):
        dateSt = str(datetime.now().strftime("%d-%m-%Y"))
        id =  self.getID()
        # getData = MainModel.getMaintenanceP(self,dateSt)
        try:
            tabletaskupdate= MainModel.getMaintenanceP(self,dateSt,id)
            self.array_item = [list(item.values())[1:] for item in tabletaskupdate]
            status_order = ['Calling', 'waiting', 'Done']
            self.array_item.sort(key=lambda row: status_order.index(row[0]) if row[0] in status_order else len(status_order))
            # tabletaskupdate = MainModel.tableTaskM(self)
            if tabletaskupdate :
                print(self.array_item)
                self.mainView.tableWidget.setRowCount(len(self.array_item))
                for row_idx, row in enumerate(self.array_item):
                    for col_idx, value in enumerate(row):
                        self.mainView.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            for i in range(7, 10):
                self.mainView.tableWidget.setColumnWidth(i, 250)
        except Exception as e :
            tabletaskupdate=[]
            self.array_item=[]

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
        self.timerT.timeout.connect(self.allTask)
        # self.timerT.timeout.connect(self.mtcPerfomance)
        self.timerT.start(5000)

    def getUsername(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("username")

    def getNote(self):
        id = self.getID()
        username = self.getUsername()
        try :
            getnote = addNote.getnote(self,id,username)
            notes_text = ""
            if getnote:
                for row in getnote:
                    date = row["datenote"] 
                    subject = row["subject"]
                    note = row["notetext"]
                    notes_text += f"- {date} ({subject})\n{note}\n\n"
                self.mainView.textBrowser.setText(notes_text)
        except Exception as e:
            getnote=[]

    
    def allTask(self):
        id = self.getID()
        try:
            getaltask = MainModel.getAllTask(self,id)
            alltask_data = [list(item.values())[1:] for item in getaltask]
            
            if getaltask :
                self.mainView.tableWidget_2.setRowCount(len(alltask_data))
                for row_idx, row in enumerate(alltask_data):
                    for col_idx, value in enumerate(row):
                        self.mainView.tableWidget_2.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            for i in range(7, 10):
                self.mainView.tableWidget_2.setColumnWidth(i, 250)

        except Exception as e:
            getaltask=[]




        



    

        







        

        