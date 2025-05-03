import sys
from PyQt6.QtWidgets import QApplication
from views.view import loginView,registerWindow,mainView,callWindowView
from controllers.controller import logincontroller,registerwindowcontroller,mainWinC,callWindowController


class appcontext:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loginwindow = None
        self.mainwindow = None
        
    
    def open_loginwindow(self):
        loginv = loginView()
        controller = logincontroller(loginv,self)
        self.loginwindow = loginv
        self.loginwindow.show()


    def openregisterWindow(self):
        registerw = registerWindow()
        controller = registerwindowcontroller(registerw,self)
        self.registerW =registerw
        self.registerW.show()
    
    def openmainWindow(self,getUsername):
        # self.getUsername = logincontroller.logincontrolBtn(self)
        mainv = mainView(getUsername)
        controller = mainWinC(mainv,self)
        self.mainv = mainv
        self.mainv.show()
    
    def callWindow(self):
        callV = callWindowView()
        controller = callWindowController(callV,self)
        self.callv = callV
        self.callv.show()
        
                

    def run(self):
        self.open_loginwindow()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    context = appcontext()
    context.run()
        


