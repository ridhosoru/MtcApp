import sys
from PyQt6.QtWidgets import QApplication
from views.view import loginView,registerWindow
from controllers.controller import logincontroller,registerwindowcontroller


class appcontext:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loginwindow = None
        self.mainwindow = None
    
    def open_loginwindow(self):
        view = loginView()
        controller = logincontroller(view,self)
        self.loginwindow = view
        self.loginwindow.show()


    def openregisterWindow(self):
        registerw = registerWindow()
        controller = registerwindowcontroller(registerw,self)
        self.registerW =registerw
        self.registerW.show()
                

    def run(self):
        self.open_loginwindow()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    context = appcontext()
    context.run()
        


