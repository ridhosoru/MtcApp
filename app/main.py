import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from views.view import (
    loginView, registerWindow, mainView, callWindowView, responView,
    closeresponView, startedView, NoteWindow, addStoreWindow,
    conTakePart, addStock
)


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


class appcontext:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = {}
        self.controllers = {}
        if not self.checkDoubleApp("MaintenanceAppLock"):
            QMessageBox.warning(None, "Warning", "Application already running.")
            sys.exit(0)
   
    def open_window_safely(self, key, view_class, controller_class, *controller_args):
        
        win = self.windows.get(key)

        
        if win is not None and not win.isVisible():
            self.windows[key] = None
            win = None

        if win is None:
            
            win = view_class()
            controller = controller_class(win, *controller_args)

            
            self.windows[key] = win
            self.controllers[key] = controller

           
            win.destroyed.connect(lambda: self.windows.update({key: None}))

            win.show()
        else:
            win.activateWindow()
            win.raise_()

   
    def openStarted(self):
        self.open_window_safely("started", startedView, startedC, self)

    def open_loginwindow(self):
        self.open_window_safely("login", loginView, logincontroller, self)

    def openregisterWindow(self):
        self.open_window_safely("register", registerWindow, registerwindowcontroller, self)

    def openmainWindow(self):
        self.open_window_safely("main", mainView, mainWinC, self)

    def openNote(self):
        self.open_window_safely("note", NoteWindow, noteCon, self)

    def openAddStore(self):
        self.open_window_safely("addStore", addStoreWindow, addStoreConn, self)

    def openTakePart(self, namepart, stock, codepart, typepart):
        self.open_window_safely("takePart", conTakePart, takePartC,
                                namepart, stock, codepart, typepart, self)

    def openaddStock(self, namepart, stock, codepart, typepart):
        self.open_window_safely("addStock", addStock, addStockC,
                                self, namepart, stock, codepart, typepart)

    def callWindow(self):
        self.open_window_safely("call", callWindowView, callWindowController, self)

    def responseWindow(self):
        self.open_window_safely("response", responView, responseWindowController, self)

    def closeCallWindow(self):
        self.open_window_safely("closeCall", closeresponView, closeRcontroller, self)

 
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
        except Exception:
            return None

    def handle_koneksi(self, blocking=True):
        if self.try_conn():
            return True

        if blocking:
            while True:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Connection Fail")
                msg.setText("Fail Connect to Server.\nMake sure it is connected to the network.")
                retry_button = msg.addButton("Try", QMessageBox.ButtonRole.AcceptRole)
                exit_button = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
                msg.exec()

                if msg.clickedButton() == exit_button:
                    sys.exit()
                if self.try_conn():
                    return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Connection Fail")
            msg.setText("Lost Connection\nTry connect or Close Application.")
            retry_button = msg.addButton("Try", QMessageBox.ButtonRole.AcceptRole)
            exit_button = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
            msg.exec()

            if msg.clickedButton() == exit_button:
                sys.exit()
            else:
                return self.handle_koneksi(blocking=True)

        return True

    def setupAutoRefresh(self):
        self.timerT = QTimer()
        self.timerT.timeout.connect(lambda: self.handle_koneksi(blocking=False))
        self.timerT.start(5000)
    
    def checkDoubleApp(self, key="MyUniqueAppKey"):
        socket = QLocalSocket()
        socket.connectToServer(key)
        if socket.waitForConnected(100): 
            return False
        self.single_instance_server = QLocalServer()
        self.single_instance_server.listen(key)
        return True

if __name__ == "__main__":
    context = appcontext()
    context.run()
