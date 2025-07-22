from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os,json
import shutil
from models.model import store

class addStoreConn:
    def __init__(self,adstore,appcontext):
        self.adstore = adstore
        self.appcontextw = appcontext
        self.storecontroller()
        
        

    def storecontroller(self):
        self.storeBtnController()

    def storeBtnController(self):
        self.adstore.cancelBtn.clicked.connect(self.cancelStore)
        self.adstore.imBtn.clicked.connect(self.importImage)
        self.adstore.addBtn.clicked.connect(self.addimStore)
    
    
    def cancelStore(self):
        self.adstore.close()
    
    def importImage(self):
        fdialog = QFileDialog()
        self.file_path, _ = fdialog.getOpenFileName(self.adstore, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        if self.file_path :
            pixmap = QPixmap(self.file_path)
            scaled_pixmap = pixmap.scaled(
                self.adstore.imageLbl.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.adstore.imageLbl.setPixmap(scaled_pixmap)
    
    def saveimg(self,codePart):
        img = self.file_path
        self.folderImg = "storeimg"
        os.makedirs(self.folderImg, exist_ok=True)
        file_name = codePart+".jpg"
        destination = os.path.join(self.folderImg, file_name)
        shutil.copy(img, destination)
    
    def addimStore(self):
        namePart= self.adstore.namePartLine.text()
        codePart= self.adstore.codeLine.text()
        typePart = self.adstore.typeLine.text()
        stockPart = self.adstore.stockLine.text()
        id = self.getID()
        self.saveimg(codePart)
        imgPath = self.folderImg+"/"+codePart+".jpg"
        
        sendAdstore = store.addstore(self,id,namePart,codePart,typePart,stockPart,imgPath)
        if sendAdstore :
            self.adstore.namePartLine.setText("")
            self.adstore.codeLine.setText("")
            self.adstore.typeLine.setText("")
            self.adstore.stockLine.setText("")
            self.adstore.imageLbl.clear()


    def getID(self):
        if os.path.exists("session.json"):
            with open("session.json", "r") as f:
                data = json.load(f)
                return data.get("id")
        

        
        