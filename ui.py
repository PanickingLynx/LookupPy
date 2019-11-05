# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'akumapy.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QMainWindow(object):
    def setupUi(self, QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(631, 464)
        QMainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.labelForPath = QtWidgets.QLabel(self.centralwidget)
        self.labelForPath.setObjectName("labelForPath")
        self.verticalLayout_3.addWidget(self.labelForPath)
        self.filePath = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath.setInputMask("")
        self.filePath.setText("")
        self.filePath.setAlignment(QtCore.Qt.AlignCenter)
        self.filePath.setObjectName("filePath")
        self.verticalLayout_3.addWidget(self.filePath)
        self.plainListRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.plainListRadio.setChecked(True)
        self.plainListRadio.setObjectName("plainListRadio")
        self.verticalLayout_3.addWidget(self.plainListRadio)
        self.textFileRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.textFileRadio.setObjectName("textFileRadio")
        self.verticalLayout_3.addWidget(self.textFileRadio)
        self.jsonFileRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.jsonFileRadio.setObjectName("jsonFileRadio")
        self.verticalLayout_3.addWidget(self.jsonFileRadio)
        self.checkNSFWService = QtWidgets.QCheckBox(self.centralwidget)
        self.checkNSFWService.setObjectName("checkNSFWService")
        self.verticalLayout_3.addWidget(self.checkNSFWService)
        self.usernameIn = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameIn.setInputMask("")
        self.usernameIn.setText("")
        self.usernameIn.setObjectName("usernameIn")
        self.verticalLayout_3.addWidget(self.usernameIn)
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setObjectName("go")
        self.verticalLayout_3.addWidget(self.go)
        QMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 22))
        self.menubar.setObjectName("menubar")
        self.menuInformation = QtWidgets.QMenu(self.menubar)
        self.menuInformation.setObjectName("menuInformation")
        QMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QMainWindow)
        self.statusbar.setObjectName("statusbar")
        QMainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuInformation.menuAction())

        self.retranslateUi(QMainWindow)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

    def retranslateUi(self, QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "AkumaPy | Forensic Search"))
        self.labelForPath.setText(_translate("QMainWindow", "Path to logfile (optional)"))
        self.plainListRadio.setText(_translate("QMainWindow", "Simple Output"))
        self.textFileRadio.setText(_translate("QMainWindow", "To .txt file"))
        self.jsonFileRadio.setText(_translate("QMainWindow", "To .json file"))
        self.checkNSFWService.setText(_translate("QMainWindow", "NSFW"))
        self.go.setText(_translate("QMainWindow", "Start the Hunt"))
        self.menuInformation.setTitle(_translate("QMainWindow", "Information"))
