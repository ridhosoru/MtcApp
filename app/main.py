import sys
import os
from PyQt6.QtWidgets import QApplication
from views.view import loginView,registerWindow,mainView,callWindowView,responView,closeresponView,startedView
from controllers.mainController import mainWinC
from controllers.loginController import logincontroller
from controllers.registerWindowController import registerwindowcontroller
from controllers.callWindowController import callWindowController
from controllers.responseWindowController import responseWindowController
from controllers.CloseRcontroller import closeRcontroller
from controllers.startedController import startedC

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
        if os.path.exists("session.json"):
            if os.path.exists("user.json"):
                self.openmainWindow()
            else:
                self.open_loginwindow()
        else:
            self.openStarted()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    context = appcontext()
    context.run()
        


