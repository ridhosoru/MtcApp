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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("login.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.closeButton.clicked.connect(self.closeApp)
        self.loginButton.clicked.connect(self.loginApp)
        self.registerButton.clicked.connect(self.registerW)

    def loginApp(self):
        usernameLogin = self.usernameLine.text()
        password = self.passwordLine.text()
        if usernameLogin or password :
            try:
                url ="http://127.0.0.1:8000/login"
                payload = {"username": usernameLogin, "password": password}
                response = requests.post(url, json=payload)
                if response.status_code == 200 :
                    print("login success")
                    QMessageBox.information(self,"Success","Login Success")
                    self.mains = mainshow(usernameLogin)
                    self.closerespon = closeresponWindow(usernameLogin)
                    self.mains.show()
                    self.close()
                else:
                    QMessageBox.warning(self,"Fail","wrong username or password")
            except Exception as e :
                QMessageBox.warning(self,"Fail",e)
        else:
            QMessageBox.warning(self,"Fail","Fill in username or password")
    
    def closeApp(self):
        closenotif = QMessageBox.question(self, 'Close Application', 'are you sure to close application?', QMessageBox.StandardButton.No| QMessageBox.StandardButton.Yes)
        if closenotif == QMessageBox.StandardButton.Yes:
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

    def registerW(self):
        self.reg = registerWindow()
        window.close()
        self.reg.show()

###################################
class registerWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("registerUser.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.backButton.clicked.connect(self.back2Log)
        self.registerButton.clicked.connect(self.regUser)
    
    def regUser(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        if username or password :
            try:
                url ="http://127.0.0.1:8000/register"
                payload = {"username": username, "password": password}
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    QMessageBox.information(self,"success","success add user")
                    self.usernameLine.clear()
                    self.passwordLine.clear()
                else :
                    QMessageBox.warning(self,"Fail","username already used")
            except Exception as e:
                QMessageBox.warning(self,"Fail",e)
        else:
            QMessageBox.warning(self,"Fail","Fill in username or password")

    def back2Log(self):
        window.show()
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

#########################################################
class mainshow(QtWidgets.QMainWindow):
    def __init__(self, usernameLogin,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        #timerdate
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(1000)
        self.usernameLogin= usernameLogin
        self.userLabel.setText("Hi, "+ self.usernameLogin)
        self.callButton.clicked.connect(self.call)
        self.callButton.setIcon(QIcon("icon/call.png"))
        self.callButton.setIconSize(QSize(32, 32))
        self.tableTask()
        self.setupAutoRefresh()
        self.callresponseButton.clicked.connect(self.callRespon)
        self.callresponseButton.setIcon(QIcon("icon/respon.png"))
        self.callresponseButton.setIconSize(QSize(32, 32))
        self.statusResponseC()
        self.closecallButton.clicked.connect(self.closerespon)
        self.closecallButton.setIcon(QIcon("icon/classcall.png"))
        self.closecallButton.setIconSize(QSize(32, 32))
        
        # self.setupAutoRefreshrS()
    
    def closerespon(self):
        self.closeR = closeresponWindow(self.usernameLogin)
        self.closeR.show()

    def statusResponseC(self):
        try:
            url= "http://127.0.0.1:8000/getstatusR"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                data_list = result.get("data", [])
                if "Calling" in data_list:
                    self.callresponseButton.setStyleSheet("background-color: red;")
                elif "waiting" in data_list:
                    self.callresponseButton.setStyleSheet("background-color: yellow;")
                else :
                    self.callresponseButton.setStyleSheet("")

        except Exception as e:
            print(e)  

    def callRespon(self,):
        self.responw = responWindow()
        self.responw.show()

    
    def tableTask(self):
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

    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.tableTask)
        self.timerT.timeout.connect(self.statusResponseC)
        self.timerT.start(3000)

    def call(self):
        self.callw = callWindow()
        self.callw.show()

    def updateDate(self):
        nowDate = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.dateLabel.setText(nowDate)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

#####################          
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

###############
class responWindow(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("responWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeW)
        self.updateTable()
        self.setupAutoRefresh()
        self.responseButton.clicked.connect(self.responsCalling)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    
    def responsCalling(self):
        selected_row = self.tableWidget.currentRow()
        data = ['status','dateSt','timeSt','timeRs','locc','machinec','probc','commentText','problemafterc','solve','timefinish','namemtc']
        rowdata={}
        if selected_row >=0 :
            #rowdata['status'] = 'waiting'
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_row, col)
                rowdata[data[col]]=item.text()
            rowdata['status'] = 'waiting'
            rowdata['timeRs'] = datetime.now().strftime("%H:%M:%S")
            try :
                url = "http://127.0.0.1:8000/updaterespon"
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

    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(self.updateTable)
        self.timerT.start(3000)


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

####
class callWindow(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("callWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.cancelButton.clicked.connect(self.closeCall)
        #########
        self.lineList()
        self.machineList()
        self.probList()
        self.okCallButton.clicked.connect(self.okCall)

    def lineList(self):
        try:
             url ="http://127.0.0.1:8000/dataLine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                self.loccomboBox.addItems(data)
        except Exception as e:
                print(e)
    
    def machineList(self):
        try:
             url ="http://127.0.0.1:8000/dataMachine"
             response = requests.get(url)
             if response.status_code == 200 :
                data = response.json()
                self.machinecomboBox.addItems(data)
        except Exception as e:
                print(e)
    
    def probList(self):
        try:
            url ="http://127.0.0.1:8000/dataProblem"
            response = requests.get(url)
            if response.status_code == 200 :
               data = response.json()
               self.probcomboBox.addItems(data)
        except Exception as e:
            print(e)

    def okCall(self):
        locc=self.loccomboBox.currentText()
        machinec=self.machinecomboBox.currentText()
        probc=self.probcomboBox.currentText()
        commentText=self.commentTextEdit.toPlainText()
        dateSt = datetime.now().strftime("%d-%m-%Y")
        timeSt = datetime.now().strftime("%H:%M:%S")
        timeRs = "-"
        status = "Calling"
        solve = "-"
        problemafterc="-"
        timefinish="-"
        namemtc="-"
        try:
            url = "http://127.0.0.1:8000/taskInput"
            payload = {"status": status, 
                       "datestart": dateSt,
                       "timestart": timeSt,
                       "timerespon": timeRs,
                       "location": locc,
                       "machine": machinec,
                       "problem": probc,
                       "commenttxt": commentText,
                       "problemaftercheck": problemafterc,
                       "solve": solve,
                       "timefinish": timefinish,
                       "namemtc": namemtc}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("success")
                self.close()
            else :
                print(response.status_code)
        except Exception as e:
            print(e)

    def closeCall(self):
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

    
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()