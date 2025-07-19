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
    
    def closeadstock(self):
        self.adstock.close()