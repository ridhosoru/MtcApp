from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel,responModel,closeCModel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt,QPoint, QTimer
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem

class logincontroller:
    def __init__(self,loginv,appcontext):
        self.loginv = loginv
        self.appcontextw = appcontext
        self.logincontroll()
    
    def logincontroll(self):
        self.loginv.loginButton.clicked.connect(self.logincontrolBtn)
        self.loginv.registerButton.clicked.connect(self.registerBtn)
        self.loginv.closeButton.clicked.connect(self.closeLogin)
    
    def closeLogin(self):
        self.loginv.close()

    def logincontrolBtn(self):
        username = self.loginv.usernameLine.text()
        password = self.loginv.passwordLine.text()
        try:
            if username and password :
                logincheck = loginmodel()
                logindata = logincheck.login(username,password)
                if logindata:
                    getUsername = logindata["username"]
                    self.appcontextw.getuser= getUsername
                    self.appcontextw.openmainWindow(getUsername)
                    self.loginv.close()
                else :
                    QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
            else :
                QMessageBox.warning(self.loginv,"Fail","Fill in username or password")
        except Exception as e:
            print(e)
    
    def registerBtn(self):
        self.appcontextw.openregisterWindow()
        self.loginv.close()

class registerwindowcontroller:
    def __init__(self,registerw,appcontext):
        self.registerw = registerw
        self.appcontextw = appcontext
        self.registercontroll()
    
    def registercontroll(self):
        self.registerw.backButton.clicked.connect(self.back2log)
        self.registerw.registerButton.clicked.connect(self.registerU)

    def back2log(self):
        self.appcontextw.open_loginwindow()
        self.registerw.close()
    
    def registerU(self):
        username = self.registerw.usernameLine.text()
        password = self.registerw.passwordLine.text()
        if username and password :
            registeru = registermodel()
            registerdata = registeru.register(username,password)
            if registerdata :
                QMessageBox.information(self.registerw,"success","success add user")
                self.registerw.usernameLine.clear()
                self.registerw.passwordLine.clear()
            else:
                QMessageBox.warning(self.registerw,"Fail","username already used")
        else :
            QMessageBox.warning(self.registerw,"Fail","Fill in username or password")

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
        tabletaskupdate = MainModel.tableTaskM(self)
        print(tabletaskupdate)
        # sortitem = {"Calling","waiting","Done"}
        # tabletaskupdate.sort()
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
        # self.timerT.timeout.connect(self.statusResponseC)
        self.timerT.start(3000)

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
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            #rowdata['status'] = 'waiting'
            for col in range(self.responView.tableWidget.columnCount()):
                item = self.responView.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'waiting'
            rowdata['timeRs'] = datetime.now().strftime("%H:%M:%S")
            postResModel = responModel.responseCModel(self,rowdata)
            if postResModel :
                self.responView.close()
                self.appcontextw.openmainWindow(self.appcontextw.getuser)

    def updateTable(self):
        gettableM = responModel.tableModel(self)
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


        



    

        







        

        