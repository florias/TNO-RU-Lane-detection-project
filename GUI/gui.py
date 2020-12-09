# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/MainWindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1481, 949)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 1481, 841))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.inputTab = QtGui.QWidget()
        self.inputTab.setObjectName(_fromUtf8("inputTab"))
        self.rosCoreWidget = QtGui.QWidget(self.inputTab)
        self.rosCoreWidget.setGeometry(QtCore.QRect(859, 20, 541, 341))
        self.rosCoreWidget.setObjectName(_fromUtf8("rosCoreWidget"))
        self.rosPlayWidget = QtGui.QWidget(self.inputTab)
        self.rosPlayWidget.setGeometry(QtCore.QRect(859, 400, 541, 341))
        self.rosPlayWidget.setObjectName(_fromUtf8("rosPlayWidget"))
        self.rawVideo = QtGui.QLabel(self.inputTab)
        self.rawVideo.setGeometry(QtCore.QRect(70, 50, 601, 700))
        self.rawVideo.setText(_fromUtf8(""))
        self.rawVideo.setObjectName(_fromUtf8("rawVideo"))
        self.line = QtGui.QFrame(self.inputTab)
        self.line.setGeometry(QtCore.QRect(790, 10, 20, 791))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.tabWidget.addTab(self.inputTab, _fromUtf8(""))
        self.outputTab = QtGui.QWidget()
        self.outputTab.setObjectName(_fromUtf8("outputTab"))
        self.processedVideo = QtGui.QLabel(self.outputTab)
        self.processedVideo.setGeometry(QtCore.QRect(70, 50, 581, 700))
        self.processedVideo.setText(_fromUtf8(""))
        self.processedVideo.setObjectName(_fromUtf8("processedVideo"))
        self.visualisedVideo = QtGui.QLabel(self.outputTab)
        self.visualisedVideo.setGeometry(QtCore.QRect(810, 50, 601, 700))
        self.visualisedVideo.setText(_fromUtf8(""))
        self.visualisedVideo.setObjectName(_fromUtf8("visualisedVideo"))
        self.line_2 = QtGui.QFrame(self.outputTab)
        self.line_2.setGeometry(QtCore.QRect(730, 10, 20, 791))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.tabWidget.addTab(self.outputTab, _fromUtf8(""))
        self.playButton = QtGui.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(50, 860, 61, 61))
        self.playButton.setText(_fromUtf8(""))
        self.playButton.setObjectName(_fromUtf8("playButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1481, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar)
        self.saveMenuButton = QtGui.QAction(MainWindow)
        self.saveMenuButton.setObjectName(_fromUtf8("saveMenuButton"))
        self.quitMenuButton = QtGui.QAction(MainWindow)
        self.quitMenuButton.setObjectName(_fromUtf8("quitMenuButton"))
        self.menuFile.addAction(self.saveMenuButton)
        self.menuFile.addAction(self.quitMenuButton)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inputTab), _translate("MainWindow", "Input", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.outputTab), _translate("MainWindow", "Output", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.saveMenuButton.setText(_translate("MainWindow", "Write to bag and quit", None))
        self.quitMenuButton.setText(_translate("MainWindow", "Quit", None))

