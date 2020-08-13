import requests
import re
import json
import sys
from termcolor import colored
from bs4 import BeautifulSoup
from submodules.ui import Ui_QMainWindow
from submodules.databaseInsertion import Ui_databaseInsertion
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import submodules.getTorSession as getTorSession
import submodules.testForErrors as testForErrors

#Make a local class for the main Window
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)


#Make a local class for the Database insertion window
class DBInsertion(QDialog):
    def __init__(self):
        super().__init__()
        self.databaseInsertion = Ui_databaseInsertion()
        self.databaseInsertion.setupUi(self)

errorListString = testForErrors.errorListExists()
app = QApplication(sys.argv)
insertion = QApplication(sys.argv)

#Shorten the module functions
d = DBInsertion()

w = AppWindow()

def statuscheck(req, output, mainlink, pathToLog, mainname, loggingMethod):
    linkIndex = 0
    #Translate the statuscode
    for i in mainlink:
        print(colored(mainlink[linkIndex], "cyan"))
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
            session = getTorSession.newTorSession()
            print(colored("Getting HTML document anonymously....", "yellow"))
            page = session.get(mainlink[linkIndex])
            print(colored("DONE!", "green"))
        else:
            print(colored("Getting HTML document...", "yellow"))
            page = requests.get(mainlink[linkIndex])
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
            status = ""
            print(colored("Non-Valid title found... Skipping...", "red"))

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
        linkIndex += 1
        #Give output to the main Log field
        print(colored("Outputting data....", "yellow"))
        #Write to a textfile if wanted
        if loggingMethod == "PLAINTEXT":
            print(colored("Writing to textfile in root directory...", "yellow"))
            outFileText = open(pathToLog, "w")
            outFileText.write(output)
            outFileText.close()
            print(colored("DONE!", "green"))
        #Output to json if wanted
        elif loggingMethod == "JSON":
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