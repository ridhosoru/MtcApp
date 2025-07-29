import sys
import os
from PyQt6.QtWidgets import QApplication
from views.view import loginView,registerWindow,mainView,callWindowView,responView,closeresponView,startedView,NoteWindow,addStoreWindow,conTakePart
from views.view import addStock
from controllers.mainController import mainWinC
from controllers.loginController import logincontroller
from controllers.registerWindowController import registerwindowcontroller
from controllers.callWindowController import callWindowController
from controllers.responseWindowController import responseWindowController
from controllers.CloseRcontroller import closeRcontroller
from controllers.startedController import startedC
from controllers.noteController import noteCon
from controllers.addStoreController import addStoreConn
from controllers.takePartCon import takePartC
from controllers.addStockController import addStockC
from models.model import getConn
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import  QTimer

class appcontext:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loginwindow = None
        self.mainwindow = None
        self.callV = None
        self.responseV = None
        self.closeV = None


    def openStarted(self):
        startedV = startedView()
        self.started = startedV
        self.controller = startedC(self,startedV)
        self.started.show()

    
    def open_loginwindow(self):
        loginv = loginView()
        self.controller = logincontroller(loginv,self)
        self.loginwindow = loginv
        self.loginwindow.show()


    def openregisterWindow(self):
        registerw = registerWindow()
        self.controller = registerwindowcontroller(registerw,self)
        self.registerW =registerw
        self.registerW.show()
    
    def openmainWindow(self):
        mainv = mainView()
        self.controller = mainWinC(mainv,self)
        self.mainv = mainv
        self.mainv.show()
    
    def openNote(self):
        notev = NoteWindow()
        self.controller=noteCon(notev,self)
        self.notev=notev
        self.notev.show()
    
    def openAddStore(self):
        adstore = addStoreWindow()
        self.controller=addStoreConn(adstore,self)
        self.adstore=adstore
        self.adstore.show()
    
    def openTakePart(self,namepart,stock,codepart,typepart):
        takePart = conTakePart()
        self.controller=takePartC(takePart,namepart,stock,codepart,typepart,self)
        self.takePart=takePart
        self.takePart.show()
    
    def openaddStock(self,namepart,stock,codepart,typepart):
        adstock = addStock()
        self.controller=addStockC(adstock,self,namepart,stock,codepart,typepart)
        self.adstore=adstock
        self.adstore.show()
    
    def callWindow(self):
        if self.callV is None or not self.callV.isVisible():
            self.callV = callWindowView()
            self.controller = callWindowController(self.callV,self)
            self.callV.show()
        else :
            self.callV.activateWindow()
            self.callV.raise_()

    def responseWindow(self):
        if self.responseV is None or not self.responseV.isVisible():
            self.responseV = responView()
            self.responeController = responseWindowController(self.responseV,self)
            self.responseV.show()
        else :
            self.responseV.activateWindow()
            self.responseV.raise_()
    
    def closeCallWindow(self):
        if self.closeV is None or not self.closeV.isVisible():
            self.closeV = closeresponView()
            self.closeVController = closeRcontroller(self.closeV,self)
            self.closeV.show()
        else :
            self.responseV.activateWindow()
            self.responseV.raise_()

    def run(self):
        self.handle_koneksi(blocking=True)
        self.setupAutoRefresh()  
        if os.path.exists("session.json"):
            if os.path.exists("user.json"):
                self.openmainWindow()
            else:
                self.open_loginwindow()
        else:
            self.openStarted()
        sys.exit(self.app.exec())
    
    def try_conn(self):
        try:
            return getConn.get_conn()
        except Exception as e:
            return None
    
    def handle_koneksi(self,blocking=True):
        if self.try_conn():
            return True
        if blocking:
        # Loop sampai berhasil atau user keluar
            while True:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Koneksi Gagal")
                msg.setText("Tidak dapat terhubung ke server.\nPastikan jaringan aktif.")
                retry_button = msg.addButton("Coba Lagi", QMessageBox.ButtonRole.AcceptRole)
                exit_button = msg.addButton("Keluar", QMessageBox.ButtonRole.RejectRole)
                msg.exec()

                if msg.clickedButton() == exit_button:
                    sys.exit()
                if self.try_conn():
                    return True
        else:
            # Untuk mode cek berkala (sekali saja)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Koneksi Terputus")
            msg.setText("Koneksi ke server hilang!\nCoba ulang atau keluar aplikasi.")
            retry_button = msg.addButton("Coba Lagi", QMessageBox.ButtonRole.AcceptRole)
            exit_button = msg.addButton("Keluar", QMessageBox.ButtonRole.RejectRole)
            msg.exec()

            if msg.clickedButton() == exit_button:
                sys.exit()
            else:
                return self.handle_koneksi(blocking=True) # kalau user pilih coba lagi, pakai mode blocking

        return True
    
    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(lambda: self.handle_koneksi(blocking=False))
        self.timerT.start(5000)

if __name__ == "__main__":
    context = appcontext()
    context.run()
        


