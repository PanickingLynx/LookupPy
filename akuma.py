# -*- coding: utf-8 -*-

import json
import re
import sys
import requests
import pymongo
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_QMainWindow
import qdarkstyle

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
w = AppWindow()


#Conect to Database and get modules
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]

#Sample DB Search Criteria

def hunt():
    output = ""
    name = w.ui.usernameIn.text()
    pathToLog = w.ui.filePath.text()
    # FOR loop, iteration durch jede line eine textdokuments (dictionary)
    # Ersetze gewisse buchstaben durch Zahlen in namen mit regular expression bei der circa letzten iteration
    # einträge in dictionary entweder vor oder nach username eingefügt
    for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
        json.dumps(field)
        wname = field["name"]
        wtype = field["type"]
        if w.ui.checkNSFWService.isChecked() != True and wtype == 1:
            output = output + "--------------------\n"
            output = output + "\nCENSORED\n"
        else:
            #Insert Name taken from UI Field into link with a regular expression
            carded = re.sub("WILDCARD", name, field["link"])
            respaced = re.sub("\s", "_", carded)
            req = requests.get(respaced).status_code
            output = output + "--------------------\n"
            output = output + "\n" + wname + "\n"
            output = output + respaced + "\n"
            #Check HTML Status Code first and list new Entry
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
                
    #Give output to the main Log field
    w.ui.textEdit.setText(output) 
    #Write to a textfile if wanted
    if w.ui.textFileRadio.isChecked():
        outFileText = open(pathToLog, "w")
        outFileText.write(output)
        outFileText.close()
    
    #JSON Output will go here

#Wait for start trigger
w.ui.go.clicked.connect(lambda: hunt())
w.show()
sys.exit(app.exec_())
