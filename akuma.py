# -*- coding: utf-8 -*-
import os
import sys

if not os.geteuid()==0:
    sys.exit('This script must be run as root!')

import json
import re
import platform
import requests
import pymongo
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import qdarkstyle
from ui import Ui_QMainWindow
from databaseInsertion import Ui_databaseInsertion
from termcolor import colored

def osDetection():
    currentSystem = platform.system()
    if currentSystem == "Windows":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()
    if currentSystem == "Darwin":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()

osDetection()

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

def newTorSession():
    newProxy = requests.session()
    newProxy.proxies = { 'http': 'socks5h://localhost:9050',
                        'https': 'socks5h://localhost:9050'}
    print(colored("Starting a new Tor proxy session....", "magenta"))
    return newProxy

session = newTorSession()

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.setWindowIcon(QtGui.QIcon("./mainicon.png"))

insertion = QApplication(sys.argv)
insertion.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
insertion.setWindowIcon(QtGui.QIcon("./mainicon.png"))

d = DBInsertion()

w = AppWindow()

#Connect to Database and get modules
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]
print(colored("Getting current MongoDB state...", "yellow"))

def trigger():
    w.ui.creditsTrigger.triggered.connect(lambda: showCredits())
    w.ui.go.clicked.connect(lambda: hunt())
    w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())
    print(colored("Waiting for another run...", "yellow"))

def insertToDatabase():
    d.show()
    d.accepted.connect(lambda: push())
    d.rejected.connect(lambda: trigger())
    print(colored("Showing database insertion...", "green"))

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
    print(colored("Inserting new JSON to database...", "yellow"))
    mycol.insert_one(newsite)
    colored("Inserted!", "green")
    trigger()


def namevariation(name, field):
    respaced = []
    newname = []
    if w.ui.namepath.text() == "":
        w.ui.textEdit.clear()
        w.ui.textEdit.setText("ERROR. Please give a path to a .txt File for\n automatic name variation.\n")
        print(colored("ERROR! Exiting namevariation check....", "red"))
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
            print(colored("Found a suffix...", "yellow"))
        elif "*" in lines[x]:
            prefix = lines[x]
            print(colored("Found a prefix...", "yellow"))
        newname.insert(x, prefix + name + suffix)
        carded = field["link"].format(newname[y])
        modified = re.sub("\s", "", carded)
        modified = re.sub(re.escape("*"), "", modified)
        modified = re.sub(re.escape(";"), "", modified)
        respaced.insert(x, re.sub("\n", "", modified))
        print(colored("Making one name...", "yellow"))
        x = x + 1
        y = y + 1

    x = x - 1
    y = y - 1
    if ";" in lines[x]:
        suffix = lines[x]
    print(colored("Mutating the name...", "yellow"))
    newname.insert(x, name + suffix)
    carded = field["link"].format(newname[y])
    modified = re.sub("\s", "", carded)
    modified = re.sub(re.escape("*"), "", modified)
    modified = re.sub(re.escape(";"), "", modified)
    respaced.insert(x, re.sub("\n", "", modified))
    print(colored("DONE!", "green"))
    return respaced



def hunt():
    mainname = []
    mainlink = []
    name = w.ui.usernameIn.text()
    output = ""
    pathToLog = "./{}.txt".format(w.ui.usernameIn.text())
    print(colored("Starting the hunt...", "green"))
    for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
        print(colored("Grabbing one dataset from the database....", "yellow"))
        z = 0
        if w.ui.useNameVar.isChecked():
            print(colored("Adding namevariation parameter... LETS MUTATE!", "green"))
            mainname.clear()
            mainname = namevariation(name, field)
        else:
            print(colored("No namevariation selected... SKIPPING!", "cyan"))
            mainname.clear()
            mainname.insert(0, name)
        for i in mainname:
            if w.ui.useNameVar.isChecked():
                print(colored("Starting namevariation...", "yellow"))
                mainlink = namevariation(name, field)
            else:
                mainlink.clear()
                mainlink.insert(0, field["link"].format(mainname[z]))
            json.dumps(field)
            wname = field["name"]
            wtype = field["type"]
            if w.ui.checkNSFWService.isChecked() != True and wtype == 1:
                print(colored("Censoring one result... Guess you're at work... Or in China...", "red"))
                output = output + "--------------------\n"
                output = output + "\nCENSORED\n"
                z = z + 1
            else:
                if w.ui.onTor.isChecked():
                    print(colored("Getting new Tor session... Let's go dark...", "magenta"))
                    session = newTorSession()
                    print(colored("Getting anonymous request.... Getting statuscode", "yellow"))
                    req = session.get(mainlink[z]).status_code
                    print(colored("DONE!", "green"))
                else:
                    print(colored("Grabbing new statuscode...", "yellow"))
                    req = requests.get(mainlink[z]).status_code
                    print(colored("DONE!", "green"))
                print(colored("Collecting new sampled output data...", "yellow"))
                output = output + "--------------------\n"
                output = output + "\n" + wname + "\n"
                output = output + mainlink[z] + "\n"
                print(colored("Translating statuscode....", "yellow"))
                output = statuscheck(req, output, mainlink, pathToLog, mainname)
                z = z + 1



def statuscheck(req, output, mainlink, pathToLog, mainname):
    y = 0
    for i in mainlink:
        print(colored("Testing....", "yellow"))
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
        print(colored("DONE!", "green"))
        #Look for Data suspicious of a missing profile in the html document
        if w.ui.onTor.isChecked():
            print(colored("Getting new Tor session... Let's go dark... (again)", "magenta"))
            session = newTorSession()
            print(colored("Getting HTML document anonymously....", "yellow"))
            page = session.get(mainlink[y])
            print(colored("DONE!", "green"))
        else:
            print(colored("Getting HTML document...", "yellow"))
            page = requests.get(mainlink[y])
            print(colored("DONE!", "green"))
        print(colored("Parsing HTML...", "yellow"))
        soup = BeautifulSoup(page.text, 'html.parser')
        print(colored("Looking for title...", "yellow"))
        status = soup.find('title').extract()
        print(colored("Lowering title...", "yellow"))
        status = status.text.lower()
        #Add entry

        if w.ui.saveHTML.isChecked():
            print(colored("Saving to HTML document...", "yellow"))
            #Save data from custom html tag given from UI if the option is checked
            htmlFile = open("./{}.html".format(w.ui.usernameIn.text()), "a")
            soup2 = BeautifulSoup(page.text, 'html.parser')
            deeptext = w.ui.htmlTags.text()
            htmltext = soup2.find(deeptext).extract()
            htmlFile.write(str(htmltext))
            print(colored("DONE!", "green"))
            htmlFile.close()

        if status is not None:
            print(colored("Found active HTTP Status code...", "yellow"))
            #If the website gave back a HTTP Status code, check for words suspicious of a missing page
            if "not found" in status or "missing" in status or "oops" in status or "removed" in status or "nicht gefunden" in status or "fehlt" in status or "ups" in status or "entfernt" in status or "existiert nicht" in status or "doesn't exist" in status:
                print(colored("Guessing that page may not exist...", "yellow"))
                output = output + "FAILED TO FIND!\n"
                hit = "bad"
            else:
                print(colored("Guessing that page probably exists...", "yellow"))
                output = output + "PROBABLY EXISTS!\n"
                hit = "good"
        else:
            print(colored("FATAL ERROR! Server might be down...", "red"))
            output = output + "EMPTY TITLE CODE MAYBE DOWN OR BAD HTML?\n"
            hit = "error"
        y = y + 1
        #Give output to the main Log field
        print(colored("Outputting data....", "yellow"))
        w.ui.textEdit.setText(output)
        #Write to a textfile if wanted
        if w.ui.textFileRadio.isChecked():
            print(colored("Writing to textfile in root directory...", "yellow"))
            outFileText = open(pathToLog, "w")
            outFileText.write(output)
            outFileText.close()
            print(colored("DONE!", "green"))
        if w.ui.jsonFileRadio.isChecked():
            print(colored("Writing to JSON file in root directory...", "yellow"))
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
            print(colored("DONE!", "green"))
        return output


def showCredits():
    print(colored("Showing credits... THANKS FOR TAKING A LOOK <3", "green"))
    msg = QMessageBox()
    msg.setIconPixmap(QPixmap("./mainicon.png"))
    msg.setText("People who showed me their Support:")
    msg.setWindowTitle("Credits")
    msg.setInformativeText("- Doelicious (Testing) \n- Maze aka. Black_eks (Script Icon artwork)\n")
    msg.setEscapeButton(msg.Ok)
    retval = msg.exec()
    if retval == msg.Ok:
        trigger()
        print(colored("Have fun using!", "green"))

#Wait for start trigger
w.ui.creditsTrigger.triggered.connect(lambda: showCredits())
w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())
w.ui.go.clicked.connect(lambda: hunt())
w.show()
d.hide()
print(colored("READY!", "green"))
sys.exit(app.exec_())
sys.exit(DBInsertion.exec_())
