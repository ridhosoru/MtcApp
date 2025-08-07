import random
from dotenv import load_dotenv
import json
from email.message import EmailMessage
import ssl
import smtplib
from PyQt6.QtCore import QTimer
from models.model import registerSModel, LoginSModel
from PyQt6.QtWidgets import QMessageBox
from pathlib import Path
import os


class startedC :
    def __init__(self,startedV,appcontext):
        self.startedView=startedV
        self.appcontexttw = appcontext
        self.startedContr()
    
    def startedContr(self):
        self.generate_code()
        self.buttonstartedC()
        self.getadm()
        
    
    def buttonstartedC(self):
        self.startedView.verifButton.clicked.connect(self.verifButtonC)
        self.startedView.registerBtn.clicked.connect(self.registerAcc)
        self.startedView.closeBtn.clicked.connect(self.closeW)
        self.startedView.minBtn.clicked.connect(self.minW)
        self.startedView.loginButton.clicked.connect(self.loginAcc)
    
    def minW(self):
        self.startedView.showMinimized()
    
    def closeW(self):
        self.startedView.close()
    
    def getadm(self):
        try:
            getadmdata= registerSModel.adminacc(self)
            if getadmdata:
                self.email=getadmdata[0]
                self.password = getadmdata[1]
        except Exception as e:
            QMessageBox.warning(self.startedView,"fail get adm",str(e))
    
    def verifButtonC(self):
        email = self.startedView.emailRLine.text()
        if email :
            try:
                self.startedView.verifButton.setEnabled(False)
                self.verification_code = startedC.generate_code(self)
                
                receiver_email = self.startedView.emailRLine.text()
                
                message = EmailMessage()
                message["Subject"] = "Your Verification Code"
                message["From"] = self.email
                message["To"] = receiver_email
                message.set_content(f"Your verification code is: {self.verification_code}")
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(self.email, self.password)
                    server.send_message(message)
                self.timerVerif()
            except Exception as e :
                print(e)
        else :
            QMessageBox.warning(self.startedView,"Fail","Please Input Email for Verification")
    
    def timerVerif(self):
        self.time_left = 300 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.time_left -= 1
        self.startedView.verifButton.setText(str(self.time_left))
        if self.time_left <= 0 :
            self.startedView.verifButton.setText("Verif")
            self.startedView.verifButton.setEnabled(True)
            self.timer.stop()

    def generate_code(self):
        return str(random.randint(100000,999999))

    def clearLineR(self):
        self.startedView.usernameRLine.clear()
        self.startedView.passwordRLine.clear()    
        self.startedView.emailRLine.clear()
        self.startedView.codeRLine.clear()
        self.time_left = 0 


    def registerAcc(self):
        username = self.startedView.usernameRLine.text()
        password = self.startedView.passwordRLine.text()    
        email = self.startedView.emailRLine.text()
        codeV = self.startedView.codeRLine.text()
        
        if username and password and email and codeV:
            if codeV == self.verification_code:
                try :
                    regmodel = registerSModel()
                    self.registerM = regmodel.registerS(username,password,email)
                    if isinstance(self.registerM, tuple) and self.registerM[0]:
                        message = str(self.registerM[1])
                        QMessageBox.critical(self.startedView, "Fail", message)
                        self.clearLineR()
                    else:
                        QMessageBox.information(self.startedView,"success","success add user")
                        self.clearLineR()
                except Exception as e :
                    QMessageBox.critical(self.startedView, "Fail", "error when register")
            else :
                QMessageBox.warning(self.startedView,"Fail","Your Code Verification Is Wrong")
        else :
            QMessageBox.warning(self.startedView,"Fail","Please Input Username, Password and Code Verification")

    def loginAcc(self):
        username = self.startedView.usernameL.text()
        password = self.startedView.passwordL.text()
        if username and password :
            try :
                loginmodel = LoginSModel()
                self.loginM = loginmodel.loginS(username,password)
                if self.loginM :
                    data = self.loginM[0]
                    getUsername = data['username']
                    getid = data['id']
                    self.saveLogInfo(getid,getUsername)
                    QMessageBox.information(self.startedView,"success","loginSuccess")
                    self.appcontexttw.open_loginwindow()
                    self.startedView.close()
                else :
                    message = str(self.loginM[0])
                    QMessageBox.critical(self.startedView, "Gagal", message)
            except Exception as e :
                    QMessageBox.warning(self.startedView,"Fail","Error Login")
        
        else :
            QMessageBox.warning(self.startedView,"Fail","Please Input Username and Password")
    
    def saveLogInfo(self,getid,getUsername):
        session_data = {"id":getid,"username": getUsername}
        save_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        save_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = save_dir / "session.json"
        with open(json_path, "w") as f:
            json.dump(session_data, f)


    