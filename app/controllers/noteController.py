import json,os
from models.model import addNote
from PyQt6.QtWidgets import QMessageBox

class noteCon:
    def __init__(self,notev,appcontext):
        self.notev = notev
        self.appcontextw = appcontext
        self.notecont()
    
    def notecont(self):
        self.noteConBtn()
    
    def noteConBtn(self):
        self.notev.cancelButton.clicked.connect(self.closenote)
        self.notev.addButton.clicked.connect(self.addNote)
    
    

    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")
            
    def getUsername(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("username")
    
    def addNote(self):
        username = self.getUsername()
        id = self.getID()
        subject = self.notev.subjectLine.text()
        notetext = self.notev.noteLine.toPlainText()
        try :
            addnote = addNote.sendNote(self,username,id,subject,notetext)
            if addnote :
                QMessageBox.information(self.notev,"success","success add note")
                self.appcontextw.openmainWindow()
                self.notev.close()
        
        except Exception as e :
            QMessageBox.warning(self.notev,"fail",str(e))
    

    def closenote(self):
        self.notev.close()