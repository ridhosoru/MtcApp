import random
from dotenv import load_dotenv
import os
from email.message import EmailMessage
import ssl
import smtplib
from PyQt6.QtCore import QTimer
from Model.model import registerModel
from PyQt6.QtWidgets import QMessageBox

load_dotenv()
email = os.getenv("email")
password = os.getenv("password")

class startedC :
    def __init__(self,startedView,AppW):
        self.startedView=startedView
        self.AppW=AppW
        self.startedContr()
    
    def startedContr(self):
        self.generate_code()
        self.buttonstartedC()
        
    
    def buttonstartedC(self):
        self.AppW.verifButton.clicked.connect(self.verifButtonC)
        self.AppW.registerBtn.clicked.connect(self.registerAcc)
    
    def verifButtonC(self):
        try:
            
            self.AppW.verifButton.setEnabled(False)
            self.verification_code = startedC.generate_code(self)
            print(self.verification_code)
            receiver_email = self.AppW.emailRLine.text()
            print(receiver_email)
            print(email)
            print(password)
            message = EmailMessage()
            message["Subject"] = "Your Verification Code"
            message["From"] = email
            message["To"] = receiver_email
            message.set_content(f"Your verification code is: {self.verification_code}")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.send_message(message)
            self.timerVerif()
        except Exception as e :
            print(e)
    
    def timerVerif(self):
        self.time_left = 300 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.time_left -= 1
        self.AppW.verifButton.setText(str(self.time_left))
        if self.time_left <= 0 :
            self.AppW.verifButton.setText("Verif")
            self.AppW.verifButton.setEnabled(True)
            self.timer.stop()

    def generate_code(self):
        return str(random.randint(100000,999999))

    def registerAcc(self):
        username = self.AppW.usernameRLine.text()
        password = self.AppW.passwordRLine.text()    
        email = self.AppW.emailRLine.text()
        codeV = self.AppW.codeRLine.text()
        
        if username and password and email and codeV:
            if codeV == self.verification_code:
                try :
                    regmodel = registerModel()
                    self.registerM = regmodel.registerS(username,password,email)
                    if "error" in self.registerM:
                        QMessageBox.critical(self.AppW, "Gagal", self.registerM["error"])
                    else:
                        QMessageBox.information(self.AppW,"success","success add user")
                        self.AppW.usernameRLine.clear()
                        self.AppW.passwordRLine.clear()    
                        self.AppW.emailRLine.clear()
                        self.AppW.codeRLine.clear()
                        self.time_left = 0  
                except Exception as e :
                    print(e)


    