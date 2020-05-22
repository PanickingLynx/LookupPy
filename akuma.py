# -*- coding: utf-8 -*-
#Import basic system functions
import sys
import json
import re
from termcolor import colored
import requests
import pymongo
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtGui
import qdarkstyle
from submodules.ui import Ui_QMainWindow
from submodules.databaseInsertion import Ui_databaseInsertion
import submodules.testForErrors as testForErrors
import submodules.getTorSession as getTorSession
import submodules.status as status
import submodules.showCredits as showCredits

errorListString = testForErrors.testAll()
newProxy = getTorSession.newTorSession()

#Make a local class for the main Window
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()


#Make a local class for the Database insertion window
class DBInsertion(QDialog):
    def __init__(self):
        super().__init__()
        self.databaseInsertion = Ui_databaseInsertion()
        self.databaseInsertion.setupUi(self)
        self.show()

#Get the new session
session = getTorSession.newTorSession()

#Set the looks of the main UI
app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.setWindowIcon(QtGui.QIcon("./mainicon.png"))


#Set the looks of the DB Insertion Window
insertion = QApplication(sys.argv)
insertion.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
insertion.setWindowIcon(QtGui.QIcon("./mainicon.png"))

#Shorten the module functions
d = DBInsertion()

w = AppWindow()


#Connect to Database and get the collection
MDBConn = pymongo.MongoClient("mongodb://localhost:27017/")
CurrentDB = MDBConn["AkumaPy"]
CurrentCollection = CurrentDB["links"]
print(colored("Getting current MongoDB state...", "yellow"))


#Open the Database insertion Windows
def insertToDatabase():
    d.show()
    print(colored("Showing database insertion...", "green"))


#Insert the userdata to the Database
def push():
    #Get the name and the link
    siteName = d.databaseInsertion.nameOfSite.text()
    siteLink = d.databaseInsertion.linkToSite.text()

    #Get the current value of the NSFW Checkbox
    if d.databaseInsertion.siteIsNSFW.isChecked():
        siteIsNSFW = 1
    else:
        siteIsNSFW = 0

    #Create the JSON Document
    newsite = {
        "name": siteName,
        "link": siteLink,
        "type": siteIsNSFW
        }
    print(colored("Inserting new JSON to database...", "yellow"))
    #Insert to the Database
    CurrentCollection.insert_one(newsite)
    colored("Inserted!", "green")

#Namevariation function to read the wordlist of possible prefixes and suffixes for names
def namevariation(name):
    respaced = []
    newname = []
    #Get the path for the wordlist
    if w.ui.namepath.text() == "":
        #Exit if none given
        w.ui.textEdit.clear()
        w.ui.textEdit.setText("ERROR. Please give a path to a .txt File for\n automatic name variation.\n")
        print(colored("ERROR! Exiting namevariation check....", "red"))
    #Open the file
    path = open(w.ui.namepath.text(), "r")
    lines = path.readlines()
    x = 0
    prefix = ""
    suffix = ""
    #Get all prefixes and suffixes
    for i in lines:
        if ";" in lines[x]:
            #This is a suffix
            suffix = lines[x]
            print(colored("Found a suffix...", "yellow"))
        elif "*" in lines[x]:
            #This is a prefix
            prefix = lines[x]
            print(colored("Found a prefix...", "yellow"))
        newname.insert(x, prefix + name + suffix)
        modified = re.sub("\s", "", newname[x])
        modified = re.sub(re.escape("*"), "", modified)
        modified = re.sub(re.escape(";"), "", modified)
        respaced.insert(x, re.sub("\n", "", modified))
        print(colored("Making one name...", "yellow"))
        x = x + 1

    x = x - 1
    #Only add a suffix
    if ";" in lines[x]:
        suffix = lines[x]
    print(colored("Mutating the name...", "yellow"))
    newname.insert(x, name + suffix)
    modified = re.sub("\s", "", newname[x])
    modified = re.sub(re.escape("*"), "", modified)
    modified = re.sub(re.escape(";"), "", modified)
    respaced.insert(x, re.sub("\n", "", modified))
    print(colored("DONE!", "green"))
    return respaced



def hunt():
    #Main block
    print(w.ui.jsonFileRadio.isChecked())
    mainname = []
    mainlink = []
    #Get the username
    name = w.ui.usernameIn.text()
    output = ""
    print(colored("Starting the hunt...", "green"))
    #Start grabbing links from the Database
    for field in CurrentCollection.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
        print(colored("Grabbing one dataset from the database....", "yellow"))
        z = 0
        #If namevariation is wanted
        if w.ui.useNameVar.isChecked():
            #Mutate the name
            print(colored("Adding namevariation parameter... LETS MUTATE!", "green"))
            mainname.clear()
            mainname = namevariation(name)
        #If namevariation is not wanted
        else:
            #Skip
            print(colored("No namevariation selected... SKIPPING!", "cyan"))
            mainname.clear()
            mainname.insert(0, name)
        #For every mutated name
        for i in mainname:
            if w.ui.useNameVar.isChecked():
                #Get all links
                print(colored("Starting namevariation...", "yellow"))
                mainlink.insert(z, field["link"].format(mainname[z]))
            else:
                #If no variation only get one link
                mainlink.clear()
                mainlink.insert(0, field["link"].format(mainname[z]))
            json.dumps(field)
            wname = field["name"]
            wtype = field["type"]
            #Is the output NSFW friendly?
            if w.ui.checkNSFWService.isChecked() != True and wtype == 1:
                #If its not friendly, censor all nsfw results
                print(colored("Censoring one result... Guess you're at work... Or in China...", "red"))
                output = output + "--------------------\n" + "\nCENSORED\n"
                z = z + 1
            #Continue as per usual
            else:
                #If the request uses onion routing
                if w.ui.onTor.isChecked():
                    #Get the html with the Proxy session
                    print(colored("Getting new Tor session... Let's go dark...", "magenta"))
                    session = getTorSession.newTorSession()
                    print(colored("Getting anonymous request.... Getting statuscode", "yellow"))
                    #Get the current HTTP status code
                    req = session.get(mainlink[z]).status_code
                    print(colored("DONE!", "green"))
                #If it doesnt use onion routing
                else:
                    #Get the request without a proxy
                    print(colored("Grabbing new statuscode...", "yellow"))
                    #Get the current HTTP status code
                    req = requests.get(mainlink[z]).status_code
                    print(colored("DONE!", "green"))
                #Sample the output with the recieved variables
                print(colored("Collecting new sampled output data...", "yellow"))
                output = output + "--------------------\n" + "\n" + wname + "\n"+ mainlink[z] + "\n"
                print(colored("Translating statuscode....", "yellow"))
                #Add the current HTTP Status code and translate it to User readable
                if w.ui.jsonFileRadio.isChecked():
                    pathToLog = "./{}.json".format(w.ui.usernameIn.text())
                    loggingMethod = "JSON"
                if w.ui.textFileRadio.isChecked():
                    pathToLog = "./{}.txt".format(w.ui.usernameIn.text())
                    loggingMethod = "PLAINTEXT"
                output = status.statuscheck(req, output, mainlink, pathToLog, mainname, loggingMethod)
                w.ui.textEdit.setText(output)
                z = z + 1


#Connect all buttons in the application
d.accepted.connect(lambda: push())
d.rejected.connect(lambda: d.hide())
w.ui.creditsTrigger.triggered.connect(lambda: showCredits.showCredits())
w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())
w.ui.go.clicked.connect(lambda: hunt())
#Display Windows
w.show()
d.hide()
#READY State
print(colored("READY!", "green"))
sys.exit(app.exec_())
sys.exit(DBInsertion.exec_())
