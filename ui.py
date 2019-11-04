# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'akumapy.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QMainWindow(object):
    def setupUi(self, QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(586, 464)
        QMainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainListRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.plainListRadio.setGeometry(QtCore.QRect(470, 10, 91, 17))
        self.plainListRadio.setChecked(True)
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
        self.usernameIn.setInputMask("")
        self.usernameIn.setText("")
        self.usernameIn.setObjectName("usernameIn")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(470, 390, 81, 23))
        self.go.setObjectName("go")
        self.filePath = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(460, 170, 113, 20))
        self.filePath.setInputMask("")
        self.filePath.setText("")
        self.filePath.setAlignment(QtCore.Qt.AlignCenter)
        self.filePath.setObjectName("filePath")
        self.checkNSFWService = QtWidgets.QCheckBox(self.centralwidget)
        self.checkNSFWService.setGeometry(QtCore.QRect(470, 100, 51, 16))
        self.checkNSFWService.setObjectName("checkNSFWService")
        self.labelForPath = QtWidgets.QLabel(self.centralwidget)
        self.labelForPath.setGeometry(QtCore.QRect(460, 140, 121, 20))
        self.labelForPath.setObjectName("labelForPath")
        QMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 21))
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
        self.plainListRadio.setText(_translate("QMainWindow", "Simple Output"))
        self.textFileRadio.setText(_translate("QMainWindow", "To .txt file"))
        self.jsonFileRadio.setText(_translate("QMainWindow", "To .json file"))
        self.go.setText(_translate("QMainWindow", "Start the Hunt"))
        self.checkNSFWService.setText(_translate("QMainWindow", "NSFW"))
        self.labelForPath.setText(_translate("QMainWindow", "Path to logfile (optional)"))
        self.menuInformation.setTitle(_translate("QMainWindow", "Information"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_QMainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())
