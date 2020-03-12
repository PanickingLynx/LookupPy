# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './databaseInsertion.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_databaseInsertion(object):
    def setupUi(self, databaseInsertion):
        databaseInsertion.setObjectName("databaseInsertion")
        databaseInsertion.resize(388, 207)
        self.verticalLayout = QtWidgets.QVBoxLayout(databaseInsertion)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(databaseInsertion)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.nameOfSite = QtWidgets.QLineEdit(databaseInsertion)
        self.nameOfSite.setObjectName("nameOfSite")
        self.verticalLayout.addWidget(self.nameOfSite)
        self.label_2 = QtWidgets.QLabel(databaseInsertion)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.linkToSite = QtWidgets.QLineEdit(databaseInsertion)
        self.linkToSite.setObjectName("linkToSite")
        self.verticalLayout.addWidget(self.linkToSite)
        self.siteIsNSFW = QtWidgets.QCheckBox(databaseInsertion)
        self.siteIsNSFW.setObjectName("siteIsNSFW")
        self.verticalLayout.addWidget(self.siteIsNSFW)
        self.buttonBox = QtWidgets.QDialogButtonBox(databaseInsertion)
        self.buttonBox.setToolTip("")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(databaseInsertion)
        self.buttonBox.accepted.connect(databaseInsertion.accept)
        self.buttonBox.rejected.connect(databaseInsertion.reject)
        QtCore.QMetaObject.connectSlotsByName(databaseInsertion)

    def retranslateUi(self, databaseInsertion):
        _translate = QtCore.QCoreApplication.translate
        databaseInsertion.setWindowTitle(_translate("databaseInsertion", "New Site"))
        self.label.setText(_translate("databaseInsertion", "Name of site:"))
        self.nameOfSite.setToolTip(_translate("databaseInsertion", "Name of the site to be added."))
        self.label_2.setText(_translate("databaseInsertion", "Link to site:"))
        self.linkToSite.setToolTip(_translate("databaseInsertion", "Link to the Website (e.g. https://example.com/{}) The {} is where the username would be."))
        self.siteIsNSFW.setToolTip(_translate("databaseInsertion", "Check this if the site is for Adult audiences."))
        self.siteIsNSFW.setText(_translate("databaseInsertion", "NSFW Site"))
