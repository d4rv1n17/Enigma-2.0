# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'enigma.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


#imports
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QShortcut
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence, QImage, QPixmap 
from PyQt5.QtCore import QThread, QTime, QTimer
from PyQt5 import uic





class Ui_Enigma(object):
    def setupUi(self, Enigma):
        Enigma.setObjectName("Enigma")
        Enigma.setEnabled(True)
        width = 1206
        height = 905        
        Enigma.resize(width, height)
        font = QtGui.QFont()
        font.setPointSize(16)
        Enigma.setFont(font)
        Enigma.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Enigma.setStyleSheet("")
        Enigma.setWindowIcon(QtGui.QIcon('enigma_window_logo.jpg'))
        self.centralwidget = QtWidgets.QWidget(Enigma)
        self.centralwidget.setStyleSheet("background-color: black\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.ep = QPixmap("Enigma_logo.png")
        self.label.setGeometry(QtCore.QRect(20, 20, 221, 91))
        font = QtGui.QFont()
        font.setFamily("Genesys")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white\n"
"")
        self.label.setText("")
        self.label.setPixmap(self.ep)
        #self.label.setPixmap(QtGui.QPixmap("../Pictures/enigma 228 100.png"))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(260, 20, 741, 221))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.textBrowser.setFont(font)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setStyleSheet("color: #c3c3c3;\n"
"border: 0px solid #000000;\n"
"")
        self.textBrowser.setObjectName("textBrowser")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 570, 371, 331))
        self.label_4.setStyleSheet("QLabel {\n"
"border-radius: 20;\n"
"}")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(360, 260, 501, 181))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(54)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color: white;\n"
"border: 0px solid #000000;\n"
"")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        #self.lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 200, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(900, 280, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: #bfbfbf")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(900, 370, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: #bfbfbf\n"
"")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1000, 630, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: #bfbfbf")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1000, 680, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: #bfbfbf")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1000, 730, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: #bfbfbf")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(1000, 780, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: #bfbfbf")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(1000, 830, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(21)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: #bfbfbf")
        self.label_11.setObjectName("label_11")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(1030, 570, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(22)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #ffffff;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.internet = QPixmap("int_con.png")
        self.no_internet = QPixmap("noint_con.png")
        self.label_12.setGeometry(QtCore.QRect(1100, 50, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: #bfbfbf")
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(70, 250, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 300, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_5.setFlat(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(70, 350, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_6.setFlat(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(70, 400, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_7.setFlat(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(70, 450, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_8.setFlat(False)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(70, 500, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_9.setFlat(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(70, 550, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_11.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_11.setFlat(False)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(70, 600, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        self.pushButton_12.setFont(font)
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_12.setStyleSheet("QPushButton {\n"
"    color: black;\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 15;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f1d500;\n"
"}")
        self.pushButton_12.setFlat(False)
        self.pushButton_12.setObjectName("pushButton_12")
        Enigma.setCentralWidget(self.centralwidget)

        self.retranslateUi(Enigma)
        QtCore.QMetaObject.connectSlotsByName(Enigma)

    def retranslateUi(self, Enigma):
        _translate = QtCore.QCoreApplication.translate
        Enigma.setWindowTitle(_translate("Enigma", "Enigma"))
        self.textBrowser.setHtml(_translate("Enigma", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nirmala UI\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.lineEdit.setText(_translate("Enigma", "00:00:00:00"))
        self.pushButton_3.setText(_translate("Enigma", "Pyraminx"))
        self.label_5.setText(_translate("Enigma", "ao5:"))
        self.label_6.setText(_translate("Enigma", "ao12:"))
        self.label_7.setText(_translate("Enigma", "1."))
        self.label_8.setText(_translate("Enigma", "2."))
        self.label_9.setText(_translate("Enigma", "3."))
        self.label_10.setText(_translate("Enigma", "4."))
        self.label_11.setText(_translate("Enigma", "5."))
        self.pushButton_10.setText(_translate("Enigma", "Reset"))
        self.pushButton_4.setText(_translate("Enigma", "2x2x2"))
        self.pushButton_5.setText(_translate("Enigma", "3x3x3"))
        self.pushButton_6.setText(_translate("Enigma", "4x4x4"))
        self.pushButton_7.setText(_translate("Enigma", "5x5x5"))
        self.pushButton_8.setText(_translate("Enigma", "6x6x6"))
        self.pushButton_9.setText(_translate("Enigma", "7x7x7"))
        self.pushButton_11.setText(_translate("Enigma", "Skewb"))
        self.pushButton_12.setText(_translate("Enigma", "Megaminx"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Enigma = QtWidgets.QMainWindow()
    ui = Ui_Enigma()
    ui.setupUi(Enigma)
    Enigma.show()
    sys.exit(app.exec_())
