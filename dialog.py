# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\AkumaPy\akumapy.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(586, 464)
        main.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setObjectName("centralwidget")
        self.plainListRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.plainListRadio.setGeometry(QtCore.QRect(470, 10, 91, 17))
        self.plainListRadio.setObjectName("plainListRadio")
        self.textFileRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.textFileRadio.setGeometry(QtCore.QRect(470, 40, 82, 17))
        self.textFileRadio.setObjectName("textFileRadio")
        self.jsonFileRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.jsonFileRadio.setGeometry(QtCore.QRect(470, 70, 82, 17))
        self.jsonFileRadio.setObjectName("jsonFileRadio")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 441, 371))
        self.textEdit.setObjectName("textEdit")
        self.usernameIn = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameIn.setGeometry(QtCore.QRect(10, 390, 441, 20))
        self.usernameIn.setObjectName("usernameIn")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(470, 390, 81, 23))
        self.go.setObjectName("go")
        self.filePath = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(470, 110, 113, 20))
        self.filePath.setInputMask("")
        self.filePath.setAlignment(QtCore.Qt.AlignCenter)
        self.filePath.setObjectName("filePath")
        main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 21))
        self.menubar.setObjectName("menubar")
        self.menuInformation = QtWidgets.QMenu(self.menubar)
        self.menuInformation.setObjectName("menuInformation")
        main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main)
        self.statusbar.setObjectName("statusbar")
        main.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuInformation.menuAction())

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "AkumaPy | Forensic Search"))
        self.plainListRadio.setText(_translate("main", "Simple Output"))
        self.textFileRadio.setText(_translate("main", "To .txt file"))
        self.jsonFileRadio.setText(_translate("main", "To .json file"))
        self.usernameIn.setText(_translate("main", "Input username here"))
        self.go.setText(_translate("main", "Start the Hunt"))
        self.filePath.setText(_translate("main", "Path to document"))
        self.menuInformation.setTitle(_translate("main", "Information"))
