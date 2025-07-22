import os,json
from datetime import datetime
from models.model import store


class addStockC:
    def __init__(self,adstock,appcontext,namepart,stock,codepart,typepart):
        self.adstock = adstock
        self.appcontextw = appcontext
        self.namepart = namepart
        self.stock = stock
        self.codepart = codepart
        self.typepart = typepart
        self.adstockcontroller()
    
    def adstockcontroller(self):
        self.adstockBtn()
        stock = self.stock
        self.adstock.stockBfLine.setText(str(stock))
        self.adstock.stockBfLine.setDisabled(True)
    
    def adstockBtn(self):
        self.adstock.cancelBtn.clicked.connect(self.closeadstock)
        self.adstock.okBtn.clicked.connect(self.updatestock)
    
    def closeadstock(self):
        self.adstock.close()

    def updatestock(self):
        id = self.getID()
        name = self.namepart
        typepart = self.typepart
        codepart = self.codepart
        qty1 = self.stock
        qty2 = int(self.adstock.stockAddLine.text())
        qtot = qty1+qty2
        user = self.getuser()
        location = "update"
        machine = "update"
        status = "update"
        date = datetime.now().strftime("%d-%m-%Y")
        storelistmodel = store.storeList(self,id,name,typepart,codepart,qty2,date,user,location,machine,status)
        takepartmodel = store.takepart(self,id,name,codepart,qtot)
        if takepartmodel :
            if storelistmodel:
                
                self.adstock.close()
                
    
    def getID(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("id")
    
    def getuser(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                data = json.load(f)
                return data.get("username")