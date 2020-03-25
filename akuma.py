# -*- coding: utf-8 -*-
#Import basic system functions
import os
import sys

#Check if the user is root
if not os.geteuid()==0:
    sys.exit('This script must be run as root!')

#Import the rest of the modules
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
    #Get current OS
    currentSystem = platform.system()
    #Exit if either is true
    if currentSystem == "Windows":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()
    if currentSystem == "Darwin":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()


#Detect the current OS
osDetection()


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


#Error list for missing indicators
try:
    errorList = open("./errorlist.txt")
    #Stringify the List to compare the words on the page with the list 
    errorListString = str(errorList)
except FileNotFoundError:
    sys.exit("errorlist.txt has not been found in the cwd, please make it by 'touch ./errorlist.txt'.")


#Get a new tor Proxy session
def newTorSession():
    #Create a session
    newProxy = requests.session()
    #Define the session
    newProxy.proxies = { 'http': 'socks5h://localhost:9050',
                        'https': 'socks5h://localhost:9050'}
    print(colored("Starting a new Tor proxy session....", "magenta"))
    return newProxy

#Get the new session
session = newTorSession()


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
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]
print(colored("Getting current MongoDB state...", "yellow"))


#Mainloop rebound
def trigger():
    print(colored("Waiting for another run...", "yellow"))


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
    mycol.insert_one(newsite)
    colored("Inserted!", "green")
    #Rebound to "mainloop"
    trigger()


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
        trigger()
    #Open the file
    path = open(w.ui.namepath.text(), "r")
    lines = path.readlines()
    x = 0
    y = 0
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
        y = y + 1

    x = x - 1
    y = y - 1
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
    mainname = []
    mainlink = []
    #Get the username
    name = w.ui.usernameIn.text()
    output = ""
    #Create a path for logging
    pathToLog = "./{}.txt".format(w.ui.usernameIn.text())
    print(colored("Starting the hunt...", "green"))
    #Start grabbing links from the Database
    for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
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
                    session = newTorSession()
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
                output = statuscheck(req, output, mainlink, pathToLog, mainname)
                z = z + 1



def statuscheck(req, output, mainlink, pathToLog, mainname):
    y = 0
    #Translate the statuscode
    for i in mainlink:
        print(colored(mainlink[y], "cyan"))
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
        #Look for Data suspicious of a missing profile in the html document
        print(colored("Parsing HTML...", "yellow"))
        soup = BeautifulSoup(page.text, 'html.parser')
        print(colored("Looking for title...", "yellow"))
        try:
            status = soup.find('title').extract()
            print(colored("Lowering title...", "yellow"))
            #Get the current html title to a parsable format
            status = status.text.lower()
        except AttributeError:
            print("Non-Valid title found... Skipping...")

        if w.ui.saveHTML.isChecked():
            print(colored("Saving to HTML document...", "yellow"))
            #Save data from custom html tag given from UI if the option is checked
            htmlFile = open("./{}.html".format(w.ui.usernameIn.text()), "a")
            #Get the html text
            soup2 = BeautifulSoup(page.text, 'html.parser')
            deeptext = w.ui.htmlTags.text()
            htmltext = soup2.find(deeptext).extract()
            htmlFile.write(str(htmltext))
            print(colored("DONE!", "green"))
            htmlFile.close()

        if status is not None:
            print(colored("Found active HTML Document...", "yellow"))
            #If the website gave back a HTTP Status code, check for words suspicious of a missing page
            if status in errorListString:
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
        #Output to json if wanted
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
    #Build and show the credits window
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


#Connect all buttons in the application
d.accepted.connect(lambda: push())
d.rejected.connect(lambda: trigger())
w.ui.creditsTrigger.triggered.connect(lambda: showCredits())
w.ui.insertionTrigger.triggered.connect(lambda: insertToDatabase())
w.ui.go.clicked.connect(lambda: hunt())
#Display Windows
w.show()
d.hide()
#READY State
print(colored("READY!", "green"))
sys.exit(app.exec_())
sys.exit(DBInsertion.exec_())
