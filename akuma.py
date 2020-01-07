# -*- coding: utf-8 -*-

import json
import re
import sys
import requests
import pymongo
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow
import qdarkstyle
from ui import Ui_QMainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.setWindowIcon("./mainicon.png")
w = AppWindow()

#Conect to Database and get modules
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]

def trigger():
    w.ui.go.clicked.connect(lambda: hunt())

#Sample DB Search Criteria
def namevariation(name, field):
    y = 0
    newname = [""]
    respaced = [""]
    if w.ui.namepath.text() == "":
        w.ui.textEdit.clear()
        w.ui.textEdit.setText("ERROR. Please give a path to a .txt File for\n automatic name variation.\n This can also be empty.\n")
        trigger()
    path = open(w.ui.namepath.text(), "r")
    lines = path.readlines()
    x = 0
    y = 1
    prefix = ""
    suffix = ""
    for i in lines:
        if ";" in lines[x]:
            suffix = lines[x]
        elif "*" in lines[x]:
            prefix = lines[x]
        newname.append(prefix + name + suffix)
        carded = re.sub("WILDCARD", newname[y], field["link"])
        modified = re.sub("\s", "_", carded)
        modified = re.sub(re.escape("*"), "", modified)
        modified = re.sub(re.escape(";"), "", modified)
        respaced.append(re.sub("\n", "", modified))
        x = x + 1
        y = y + 1
    
    return respaced

    


def hunt():
    name = w.ui.usernameIn.text()
    output = ""
    pathToLog = w.ui.filePath.text()
    
    for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
        z = 1
        for i in namevariation(name, field):
            if w.ui.useNameVar.isChecked:
                mainlink = namevariation(name, field)[z]
            else:
                mainlink = field["link"] + name
            json.dumps(field)
            wname = field["name"]
            wtype = field["type"]
            if w.ui.checkNSFWService.isChecked() != True and wtype == 1:
                output = output + "--------------------\n"
                output = output + "\nCENSORED\n"
                z = z + 1
            else:
                req = requests.get(mainlink).status_code
                output = output + "--------------------\n"
                output = output + "\n" + wname + "\n"
                output = output + mainlink + "\n"
                output = statuscheck(req, output, mainlink, pathToLog)
                z = z + 1



def statuscheck(req, output, respaced, pathToLog):
    y = 0
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
    page = requests.get(respaced)
    soup = BeautifulSoup(page.text, 'html.parser')
    status = soup.find('html').extract()
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
        if "not found" in status or "missing" in status or "oops" in status or "removed" in status or "nicht gefunden" in status or "fehlt" in status or "ups" in status or "entfernt" in status:
            output = output + "FAILED TO FIND!\n"
        else:
            output = output + "PROBABLY EXISTS!\n"
    else:
        output = output + "EMPTY TITLE CODE MAYBE DOWN OR BAD HTML?\n"
    y = y + 1
    #Give output to the main Log field
    w.ui.textEdit.setText(output) 
    #Write to a textfile if wanted
    if w.ui.textFileRadio.isChecked():
        outFileText = open(pathToLog, "w")
        outFileText.write(output)
        outFileText.close()
    return output
    #JSON Output will go here

#Wait for start trigger
w.ui.go.clicked.connect(lambda: hunt())
w.show()
sys.exit(app.exec_())
