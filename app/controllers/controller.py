from views.view import loginView
from models.model import loginmodel,registermodel,MainModel,callWModel
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

    def logincontrolBtn(self):
        username = self.loginv.usernameLine.text()
        password = self.loginv.passwordLine.text()
        try:
            if username and password :
                logincheck = loginmodel()
                logindata = logincheck.login(username,password)
                if logindata:
                    getUsername = logindata["username"]
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
    
    def callButtonA(self):
        self.appcontextw.callWindow()

    def tabletask(self):
        tabletaskupdate = MainModel.tableTaskM(self)
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
    #     self.callControllerButton()
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
    
    # def callControllerButton(self):
    #     print(0)
    #     self.callWindowView.cancelButton.clicked.connect(self.closeCall)
    
    # def closeCall(self):
    #     self.close()
    

        



    

        







        

        