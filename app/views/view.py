
from PyQt6 import  QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt,QPoint, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import requests

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class loginView(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/login.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

class registerWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/registerUser.ui", self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
        

class mainView(QtWidgets.QMainWindow):
    def __init__(self,getusername, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/mainwindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.usernameLogin= getusername
        self.userLabel.setText("Hi, "+ self.usernameLogin)
        self.callButton.setIcon(QIcon("icon/call.png"))
        self.callButton.setIconSize(QSize(32, 32))
        self.callresponseButton.setIcon(QIcon("icon/respon.png"))
        self.callresponseButton.setIconSize(QSize(32, 32))
        self.closecallButton.setIcon(QIcon("icon/classcall.png"))
        self.closecallButton.setIconSize(QSize(32, 32))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

class callWindowView(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/callWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

class responView(QtWidgets.QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/responWindow.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dragPos = None
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()