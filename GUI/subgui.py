# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/SubWindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(240, 136)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 191, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.loadBag = QtGui.QPushButton(Dialog)
        self.loadBag.setGeometry(QtCore.QRect(10, 60, 97, 27))
        self.loadBag.setObjectName(_fromUtf8("loadBag"))
        self.liveSource = QtGui.QPushButton(Dialog)
        self.liveSource.setGeometry(QtCore.QRect(120, 60, 111, 27))
        self.liveSource.setObjectName(_fromUtf8("liveSource"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Source selection", None))
        self.label.setText(_translate("Dialog", "Please select an option:", None))
        self.loadBag.setText(_translate("Dialog", "Load bag file", None))
        self.liveSource.setText(_translate("Dialog", "Use live source", None))

