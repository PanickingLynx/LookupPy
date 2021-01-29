from termcolor import colored
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap

def showCredits():
    #Build and show the credits window
    print(colored("Showing credits... THANKS FOR TAKING A LOOK <3", "green"))
    msg = QMessageBox()
    msg.setIconPixmap(QPixmap("./mainicon.png"))
    msg.setText("People who showed me their Support:")
    msg.setWindowTitle("Credits")
    msg.setInformativeText("- Doelicious (Testing) \n")
    msg.setEscapeButton(msg.Ok)
    retval = msg.exec()
    if retval == msg.Ok:
        print(colored("Have fun using!", "green"))