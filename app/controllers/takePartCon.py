import os,json
from models.model import callWModel
from datetime import datetime
from models.model import store
from pathlib import Path

class takePartC:
    def __init__(self,takePart,namepart,stock,codepart,typepart,appcontext):
        self.takePart = takePart
        self.appcontextw = appcontext
        self.namepart = namepart
        self.stock = stock
        self.codepart = codepart
        self.typepart = typepart
        self.takepartcon()
        
    
    def takepartcon(self):
        self.takpartconBtn()
        self.takepartw()

    def takepartw(self):
        name = self.namepart
        qty1 = self.stock
        self.takePart.namepartL.setText(name)
        self.lineList()
        self.machineList()
        
    
    def takpartconBtn(self):
        self.takePart.cancelBtn.clicked.connect(self.closetakepart)
        self.takePart.okBtn.clicked.connect(self.oktakepart)
    
    def oktakepart(self):
        id = self.getID()
        name = self.namepart
        typepart = self.typepart
        codepart = self.codepart
        qty1 = self.stock
        qty2 = int(self.takePart.qtyLine.text())
        qtot = qty1-qty2
        user = self.getuser()
        location = self.takePart.loccombobox.currentText()
        machine = self.takePart.machinecombobox.currentText()
        status = "take"
        date = datetime.now().strftime("%d-%m-%Y")
        storelistmodel = store.storeList(self,id,name,typepart,codepart,qty2,date,user,location,machine,status)
        takepartmodel = store.takepart(self,id,name,codepart,qtot)
        if takepartmodel :
            if storelistmodel:
                self.takePart.close()
                
    
    def closetakepart(self):
        self.takePart.close()
    
    def getID(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            with open(user_path, "r") as f:
                data = json.load(f)
                return data.get("id")
    
    def getuser(self):
        appdata_dir = Path(os.getenv("LOCALAPPDATA")) / "MaintenanceApp"
        user_path = appdata_dir / "user.json"
        if user_path.exists():
            with open(user_path, "r") as f:
                data = json.load(f)
                return data.get("username")
            
    def lineList(self):
        id = int(self.getID())
        linegetm = callWModel.linemodel(self,id)
        if linegetm :
            name_list = [item['name'] for item in linegetm]
            self.takePart.loccombobox.clear()
            self.takePart.loccombobox.addItems(name_list)

    def machineList(self):
        id = int(self.getID())
        machinegetm = callWModel.machinemodel(self,id)
        if machinegetm :
            name_list = [item['name'] for item in machinegetm]
            self.takePart.machinecombobox.clear()
            self.takePart.machinecombobox.addItems(name_list)
