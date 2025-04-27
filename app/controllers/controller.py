from views.view import loginView
from models.model import loginmodel,registermodel
from PyQt6.QtWidgets import QMessageBox

class logincontroller:
    def __init__(self,view,appcontext):
        self.view = view
        self.appcontextw = appcontext
        self.logincontroll()
    
    def logincontroll(self):
        self.view.loginButton.clicked.connect(self.logincontrolBtn)
        self.view.registerButton.clicked.connect(self.registerBtn)

    def logincontrolBtn(self):
        username = self.view.usernameLine.text()
        password = self.view.passwordLine.text()
        if username and password :
            logincheck = loginmodel()
            logindata = logincheck.login(username,password)
            if logindata:
                self.appcontextw.openmainWindow(logindata["username"])
                self.view.close()
            else :
                QMessageBox.warning(self.view,"Fail","Fill in username or password")
        else :
            QMessageBox.warning(self.view,"Fail","Fill in username or password")
    
    def registerBtn(self):
        self.appcontextw.openregisterWindow()
        self.view.close()

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

    

        







        

        