from PyQt6.QtWidgets import (
    QMessageBox, QLabel, QVBoxLayout, QPushButton, QWidget, QFrame,
    QGridLayout, QHBoxLayout, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor
from datetime import datetime
import os, json
from functools import partial
from pathlib import Path
from models.model import MainModel, addNote, Regprod, store

class AutoRefreshThread(QThread):
    dataUpdated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__()
        self.running = True
        self.parent = parent

    def run(self):
        while self.running:
            try:
                id_user = self.parent.getID()
                username = self.parent.getUsername()
                dateSt = str(datetime.now().strftime("%d-%m-%Y"))

                data = {
                    "task": MainModel.getMaintenanceP(self.parent, dateSt, id_user),
                    "alltask": MainModel.getAllTask(self.parent, id_user),
                    "store": store.getStore(self.parent, id_user),
                    "storeAct": store.getAllStoreAct(self.parent, id_user),
                    "note": addNote.getnote(self.parent, id_user, username)
                }

                self.dataUpdated.emit(data)
            except:
                pass

            self.msleep(5000)  

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class mainWinC:
    def __init__(self, mainView, appcontext):
        self.mainView = mainView
        self.appcontextw = appcontext
        self.array_item = []
        self.mainWindowController()

    def mainWindowController(self):
        self.mainWindowButtonController()
        self.timerU()
        self.tabletask()
        self.mtcPerfomance()
        self.regProdPage()

        self.refreshThread = AutoRefreshThread(self)
        self.refreshThread.dataUpdated.connect(self.updateFromThread)
        self.refreshThread.start()

    def updateFromThread(self, data):
        self.updateTask(data["task"])
        self.updateAllTask(data["alltask"])
        self.updateStore(data["store"])

        if self.mainView.stackedWidget.currentIndex() == 4:
            self.updateStoreActivity(data["storeAct"])

        self.updateNote(data["note"])
        self.mtcPerfomance()

        self.getStatusR()

    def updateTask(self, tabletaskupdate):
        try:
            self.array_item = [list(item.values())[1:] for item in tabletaskupdate]
            status_order = ['Calling', 'waiting', 'Done']
            self.array_item.sort(
                key=lambda row: status_order.index(row[0]) if row[0] in status_order else len(status_order)
            )

            self.mainView.tableWidget.setRowCount(len(self.array_item))
            for row_idx, row in enumerate(self.array_item):
                for col_idx, value in enumerate(row):
                    self.mainView.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except:
            self.array_item = []

    def updateAllTask(self, alltask_data):
        try:
            rows = [list(item.values())[1:] for item in alltask_data]
            self.mainView.tableWidget_2.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.mainView.tableWidget_2.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except:
            pass

    def updateStore(self, getmodel):
        if getmodel:
            self.displaybox(getmodel)

    def updateStoreActivity(self, getallstore):
        try:
            fields = [
                "namepart", "codepart", "typepart", "prodtake",
                "date", "nameuser", "location", "machine", "status"
            ]
            data = [[item.get(field, "") for field in fields] for item in getallstore]
            self.mainView.tableWidget_3.setRowCount(len(data))
            self.mainView.tableWidget_3.setColumnCount(len(fields))

            for row_idx, row in enumerate(data):
                status_value = row[fields.index("status")].lower().strip()
                if status_value == "update":
                    bg_color = QColor(144, 238, 144)
                elif status_value == "take":
                    bg_color = QColor(240, 128, 128)
                else:
                    bg_color = QColor(255, 255, 255)

                for col_idx, value in enumerate(row):
                    item_widget = QTableWidgetItem(str(value))
                    item_widget.setBackground(bg_color)
                    self.mainView.tableWidget_3.setItem(row_idx, col_idx, item_widget)
        except:
            pass

    def updateNote(self, getnote):
        try:
            notes_text = ""
            for row in getnote:
                notes_text += f"- {row['datenote']} ({row['subject']})\n{row['notetext']}\n\n"
            self.mainView.textBrowser.setText(notes_text)
        except:
            pass

    def mtcPerfomance(self):
        self.totalTask()
        self.taskWaiting()
        self.taskComplete()
        self.avgTimeRespon()
        self.avgTimeComplete()

    def totalTask(self):
        if self.array_item:
            self.mainView.label_totTask.setText("TOTAL TASK : " + str(len(self.array_item)))

    def taskWaiting(self):
        if self.array_item:
            waiting = [row[0] for row in self.array_item].count('waiting')
            self.mainView.label_taskWaiting.setText("TASK WAITING : " + str(waiting))

    def taskComplete(self):
        if self.array_item:
            done = [row[0] for row in self.array_item].count('Done')
            self.mainView.label_taskComplete.setText("TASK COMPLETE: " + str(done))

    def avgTimeComplete(self):
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

    def avgTimeRespon(self):
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

    def getStatusR(self):
        
        self.mainView.callresponseButton.setStyleSheet("")
        self.mainView.closecallButton.setStyleSheet("")

        if not self.array_item:
            return

        status_list = [row[0] for row in self.array_item]

        
        if "Calling" in status_list:
            self.mainView.callresponseButton.setStyleSheet("background-color: yellow;")

        
        if "waiting" in status_list:
            self.mainView.closecallButton.setStyleSheet("background-color: yellow;")

    def mainWindowButtonController(self):
        self.mainView.callButton.clicked.connect(self.callButtonA)
        self.mainView.callresponseButton.clicked.connect(self.responseButtonA)
        self.mainView.closecallButton.clicked.connect(self.closeCallA)
        self.mainView.closeButton.clicked.connect(self.closeM)
        self.mainView.minButton.clicked.connect(self.minM)
        self.mainView.logoutButton.clicked.connect(self.logout)
        self.mainView.addNButton.clicked.connect(self.openAddN)

        self.mainView.homeButton.clicked.connect(self.home)
        self.mainView.alltaskButton.clicked.connect(self.alltask)
        self.mainView.regProdBtn.clicked.connect(self.regProd)
        self.mainView.storeBtn.clicked.connect(self.store)
        self.mainView.storeActbtn.clicked.connect(self.storeAct)
        self.mainView.addstorebtn.clicked.connect(self.addstore)

    def home(self): self.mainView.stackedWidget.setCurrentIndex(0)
    def alltask(self): self.mainView.stackedWidget.setCurrentIndex(1)
    def regProd(self): self.mainView.stackedWidget.setCurrentIndex(2)
    def store(self): self.mainView.stackedWidget.setCurrentIndex(3)
    def storeAct(self): self.mainView.stackedWidget.setCurrentIndex(4)

    def regProdPage(self):
        self.mainView.machInBtn.clicked.connect(self.machineInput)
        self.mainView.locInBtn.clicked.connect(self.LocInput)
        self.mainView.probInBtn.clicked.connect(self.probInput)

    def machineInput(self):
        id = self.getID()
        name = self.mainView.machInLine.text()
        try :
            inpMach = Regprod.machineInp(self,id,name)
            if inpMach:
                QMessageBox.information(self.mainView,"success","Success add machine name")
                self.mainView.machInLine.clear()
        
        except Exception as e :
            QMessageBox.warning(self.mainView,"fail",str(e))
    
    def LocInput(self):
        id = self.getID()
        name = self.mainView.LocInLine.text()
        try :
            inpMach = Regprod.LocInp(self,id,name)
            if inpMach:
                QMessageBox.information(self.mainView,"success","Success add Location")
                self.mainView.LocInLine.clear()
        
        except Exception as e :
            QMessageBox.warning(self.mainView,"fail",str(e))

    def probInput(self):
        id = self.getID()
        name = self.mainView.probInLine.text()
        try :
            inpMach = Regprod.probInp(self,id,name)
            if inpMach:
                QMessageBox.information(self.mainView,"success","Success add Problem")
                self.mainView.probInLine.clear()
        
        except Exception as e :
            QMessageBox.warning(self.mainView,"fail",str(e))

    def displaybox(self, getmodel):
        gridlay = QGridLayout()
        gridlay.setSpacing(20)
        for index, item in enumerate(getmodel):
            framePart = QFrame()
            framePart.setFixedWidth(200)
            framePart.setFixedHeight(250)
            framePart.setObjectName("framepart")
            framePart.setStyleSheet("QFrame#framepart{background-color:#40916c;border-radius:10px;}")

            vbox = QVBoxLayout()
            vbox.addWidget(QLabel(f"NamePart: {item['namepart']}"))
            vbox.addWidget(QLabel(f"Code: {item['codepart']}"))
            vbox.addWidget(QLabel(f"Type: {item['typepart']}"))
            vbox.addWidget(QLabel(f"Stock: {item['stockpart']}"))

            img_label = QLabel()
            img_path = item["imgpath"]
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                img_label.setPixmap(pixmap)
            else:
                img_label.setText("Gambar tidak ditemukan")
            vbox.addWidget(img_label)

            hbox = QHBoxLayout()
            Tbtn = QPushButton("Take Product")
            Tbtn.clicked.connect(partial(self.takeProduct, item))
            Ubtn = QPushButton("Update Stock")
            Ubtn.clicked.connect(partial(self.updateStock, item))
            hbox.addWidget(Tbtn)
            hbox.addWidget(Ubtn)
            vbox.addLayout(hbox)

            framePart.setLayout(vbox)
            row, col = index // 4, index % 4
            gridlay.addWidget(framePart, row, col)

        container = QWidget()
        container.setLayout(gridlay)
        self.mainView.storeScrollArea.setWidget(container)

   
    def updateStock(self, item): self.appcontextw.openaddStock(item['namepart'], item['stockpart'], item['codepart'], item['typepart'])
    def takeProduct(self, item): self.appcontextw.openTakePart(item['namepart'], item['stockpart'], item['codepart'], item['typepart'])
    def openAddN(self): self.appcontextw.openNote()
    def addstore(self): self.appcontextw.openAddStore()
    def callButtonA(self): self.appcontextw.callWindow()
    def responseButtonA(self): self.appcontextw.responseWindow()
    def closeCallA(self): self.appcontextw.closeCallWindow()

    def logout(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            os.remove(user_path)
        self.refreshThread.stop()
        self.mainView.close()
        self.appcontextw.open_loginwindow()

    def closeM(self):
        self.refreshThread.stop()
        self.mainView.close()

    def minM(self): self.mainView.showMinimized()

    def getID(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            return json.load(open(user_path)).get("id")

    def getUsername(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            return json.load(open(user_path)).get("username")

    def tabletask(self): pass  

    def timerU(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(1000)

    def updateDate(self):
        self.mainView.dateLabel.setText(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
