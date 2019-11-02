import json
import re
import sys
import requests
import pymongo
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_QMainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QMainWindow()
        self.ui.setupUi(self)
        self.show()


app = QApplication(sys.argv)
w = AppWindow()
w.show()

#Conect to Database and get modules
MyClient = pymongo.MongoClient("mongodb://localhost:27017/")
MyDB = MyClient["AkumaPy"]
mycol = MyDB["links"]
name = w.ui.usernameIn.displayText()
nsfw = input("SAFE SEARCH ON? <y/n>: ")
#Sample DB Search Criteria
for field in mycol.find({}, {'_id': 0, 'name': 1, 'link': 1, 'type': 1}):
    json.dumps(field)
    wname = field["name"]
    wtype = field["type"]
    if nsfw == "y" and wtype == 1:
        break
    else:
        carded = re.sub("WILDCARD", name, field["link"])
        respaced = re.sub("\s", "_", carded)
        req = requests.get(respaced).status_code
        w.ui.textEdit.setText("--------------------")
        w.ui.textEdit.setText(wname)
        w.ui.textEdit.setText(";")
        w.ui.textEdit.setText(respaced)
        #Check HTML Status Code first and list new Entry
        if req == 200:
            print("200 OK!")
        elif req == 503:
            print("503 ERROR!")
        elif req == 403:
            print("403 DENIED!")
        elif req == 404:
            print("404 MISSING!")
        elif req == 301:
            print("301 MOVED!")
        else:
            print("TIMEOUT OR DOWN!")
        #Look for Data suspicious of a missing profile in the title
        page = requests.get(respaced)
        soup = BeautifulSoup(page.text, 'html.parser')
        status = soup.find('title').extract()
        status = status.text.lower()
        #Add entry
        if status is not None:
            if "not found" in status:
                print("FAILED TO FIND!")
            else:
                print("PROBABLY EXISTS!")
        else:
            print("EMPTY TITLE CODE MAYBE DOWN OR BAD HTML?")
            #Added some data

sys.exit(app.exec_())