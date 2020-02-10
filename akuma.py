# -*- coding: utf-8 -*-

import json
import re
import sys
import requests
import pymongo
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import qdarkstyle
from ui import Ui_QMainWindow
from databaseInsertion import Ui_databaseInsertion

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()

class DBInsertion(QDialog):
    def __init__(self):
        super().__init__()
        self.databaseInsertion = Ui_databaseInsertion()
        self.databaseInsertion.setupUi(self)
        self.show()


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.setWindowIcon(QtGui.QIcon("./mainicon.png"))

insertion = QApplication(sys.argv)
insertion.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
insertion.setWindowIcon(QtGui.QIcon("./mainicon.png"))

d = DBInsertion()

w = AppWindow()

#Conect to Database and get modules
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]

def trigger():
    w.ui.creditsTrigger.triggered.connect(lambda: showCredits())
    w.ui.go.clicked.connect(lambda: hunt())
    w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())

def insertToDatabase():
    d.show()
    d.accepted.connect(lambda: push())
    d.rejected.connect(lambda: trigger())

def push():
    siteName = d.databaseInsertion.nameOfSite.text()
    siteLink = d.databaseInsertion.linkToSite.text()

    if d.databaseInsertion.siteIsNSFW.isChecked():
        siteIsNSFW = 1
    else:
        siteIsNSFW = 0

    newsite = {
        "name": siteName,
        "link": siteLink,
        "type": siteIsNSFW
        }
    mycol.insert_one(newsite)
    trigger()


#Sample DB Search Criteria
def namevariation(name, field):
    respaced = []
    newname = []
    if w.ui.namepath.text() == "":
        w.ui.textEdit.clear()
        w.ui.textEdit.setText("ERROR. Please give a path to a .txt File for\n automatic name variation.\n")
        trigger()
    path = open(w.ui.namepath.text(), "r")
    lines = path.readlines()
    x = 0
    y = 0
    prefix = ""
    suffix = ""
    for i in lines:
        if ";" in lines[x]:
            suffix = lines[x]
        elif "*" in lines[x]:
            prefix = lines[x]
        newname.insert(x, prefix + name + suffix)
        carded = re.sub("WILDCARD", newname[y], field["link"])
        modified = re.sub("\s", "", carded)
        modified = re.sub(re.escape("*"), "", modified)
        modified = re.sub(re.escape(";"), "", modified)
        respaced.insert(x, re.sub("\n", "", modified))
        x = x + 1
        y = y + 1

    x = x - 1
    y = y - 1
    if ";" in lines[x]:
        suffix = lines[x]
    newname.insert(x, name + suffix)
    carded = re.sub("WILDCARD", newname[y], field["link"])
    modified = re.sub("\s", "", carded)
    modified = re.sub(re.escape("*"), "", modified)
    modified = re.sub(re.escape(";"), "", modified)
    respaced.insert(x, re.sub("\n", "", modified))
    return respaced



def hunt():
    mainname = []
    mainlink = []
    name = w.ui.usernameIn.text()
    output = ""
    pathToLog = w.ui.filePath.text()
    for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
        z = 0
        if w.ui.useNameVar.isChecked():
            mainname.clear()
            mainname = namevariation(name, field)
        else:
            mainname.clear()
            mainname.insert(0, name)
        for i in mainname:
            if w.ui.useNameVar.isChecked():
                mainlink = namevariation(name, field)
            else:
                mainlink.clear()
                mainlink.insert(0, re.sub("WILDCARD", mainname[z], field["link"]))
            json.dumps(field)
            wname = field["name"]
            wtype = field["type"]
            if w.ui.checkNSFWService.isChecked() != True and wtype == 1:
                output = output + "--------------------\n"
                output = output + "\nCENSORED\n"
                z = z + 1
            else:
                req = requests.get(mainlink[z]).status_code
                output = output + "--------------------\n"
                output = output + "\n" + wname + "\n"
                output = output + mainlink[z] + "\n"
                output = statuscheck(req, output, mainlink, pathToLog, mainname)
                z = z + 1



def statuscheck(req, output, mainlink, pathToLog, mainname):
    y = 0
    for i in mainlink:
        if req == 200:
            output = output + "200 OK!\n"
        elif req == 503:
            output = output + "503 ERROR!\n"
        elif req == 403:
            output = output + "403 DENIED!\n"
        elif req == 404:
            output = output + "404 MISSING!\n"
        elif req == 301:
            output = output + "301 MOVED!\n"
        else:
            output = output + "TIMEOUT OR DOWN!\n"

        #Look for Data suspicious of a missing profile in the html document
        page = requests.get(mainlink[y])
        soup = BeautifulSoup(page.text, 'html.parser')
        status = soup.find('title').extract()
        status = status.text.lower()
        #Add entry

        if w.ui.saveHTML.isChecked():
            #Save data from custom html tag given from UI if the option is checked
            soup2 = BeautifulSoup(page.text, 'html.parser')
            deeptext = w.ui.htmlTags.text()
            htmltext = soup2.find(deeptext).extract()
            htmlFile = open(w.ui.pathToHTML.text(), "w")
            htmlFile.write(str(htmltext))
            htmlFile.close()

        if status is not None:
            #If the website gave back a HTTP Status code, check for words suspicious of a missing page
            if "not found" in status or "missing" in status or "oops" in status or "removed" in status or "nicht gefunden" in status or "fehlt" in status or "ups" in status or "entfernt" in status or "existiert nicht" in status or "doesn't exist" in status:
                output = output + "FAILED TO FIND!\n"
                hit = "bad"
            else:
                output = output + "PROBABLY EXISTS!\n"
                hit = "good"
        else:
            output = output + "EMPTY TITLE CODE MAYBE DOWN OR BAD HTML?\n"
            hit = "error"
        y = y + 1
        #Give output to the main Log field
        w.ui.textEdit.setText(output)
        #Write to a textfile if wanted
        if w.ui.textFileRadio.isChecked():
            outFileText = open(pathToLog, "w")
            outFileText.write(output)
            outFileText.close()
        if w.ui.jsonFileRadio.isChecked():
            toJSON = {
                "username": mainname,
                "link": mainlink,
                "site_status": req,
                "hit": hit
            }
            textJSON = json.dumps(toJSON)
            textJSON = textJSON + "\n"
            textJSON = re.sub(", ", ", \n", textJSON)
            textJSON = re.sub("{", "{\n", textJSON)
            textJSON = re.sub("}", "\n}", textJSON)
            jfile = open(pathToLog, "a")
            jfile.write(textJSON)
            jfile.close()
        return output


def showCredits():
    msg = QMessageBox()
    msg.setIconPixmap(QPixmap("./mainicon.png"))
    msg.setText("People who showed me their Support:")
    msg.setWindowTitle("Credits")
    msg.setInformativeText("- Doelicious (Testing) \n- Maze aka. Black_eks (Script Icon artwork)\n")
    msg.setEscapeButton(msg.Ok)
    retval = msg.exec()
    if retval == msg.Ok:
        trigger()

#Wait for start trigger
w.ui.creditsTrigger.triggered.connect(lambda: showCredits())
w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())
w.ui.go.clicked.connect(lambda: hunt())
w.show()
d.hide()
sys.exit(app.exec_())
sys.exit(DBInsertion.exec_())
