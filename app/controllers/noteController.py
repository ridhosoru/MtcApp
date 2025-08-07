import json,os
from models.model import addNote
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from pathlib import Path

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
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            with open(user_path, "r") as f:
                data = json.load(f)
                return data.get("id")
            
    def getUsername(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            with open(user_path, "r") as f:
                data = json.load(f)
                return data.get("username")
    
    def addNote(self):
        username = self.getUsername()
        id = self.getID()
        subject = self.notev.subjectLine.text()
        notetext = self.notev.noteLine.toPlainText()
        datenote = datetime.now().strftime("%d-%m-%Y")
        try :
            addnote = addNote.sendNote(self,username,id,subject,notetext,datenote)
            if addnote :
                QMessageBox.information(self.notev,"success","success add note")
                self.appcontextw.openmainWindow()
                self.notev.close()
        
        except Exception as e :
            QMessageBox.warning(self.notev,"fail",str(e))
    

    def closenote(self):
        self.notev.close()