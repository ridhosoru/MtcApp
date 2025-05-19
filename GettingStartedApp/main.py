import sys
from PyQt6.QtWidgets import QApplication
from View.view import startedView
from Controller.startedController import startedC

class AppW :
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.started = None
    
    def openStarted(self):
        startedV = startedView()
        self.started = startedV
        self.controller = startedC(self,startedV)
        self.started.show()

    
    
    def run(self):
        self.openStarted()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    context = AppW()
    context.run()
        