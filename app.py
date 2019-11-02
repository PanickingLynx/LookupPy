import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from ui import Ui_QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()

def sayHello():
    w.ui.textEdit.print("NEW TEXT")
    mainloop()


app = QApplication(sys.argv)
w = AppWindow()


def mainloop():
    w.ui.textEdit.print("HELLO1")
    w.ui.go.clicked.connect(sayHello)

w.show()
mainloop()
sys.exit(app.exec_())