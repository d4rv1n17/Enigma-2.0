from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QShortcut
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence, QImage, QPixmap 
from PyQt5.QtCore import QThread, QTime, QTimer
from PyQt5 import uic
import time
import sys
import requests
import datetime
import random
from enigmaInterface import Ui_Enigma
import scram_gen as sg


"""---Enigma logic---"""    


# function to define is internet connection is available
def internet_connection():

    url_image = 'https://google.com/'

    timeout = 10
    try:
        request = requests.get(url_image, timeout=timeout)
        ui.label_12.setPixmap(ui.internet)
    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection!")


# Generation scramble and getting picture of cube 2x2x2
def cube2x2():

    global scrambleSellection
    scrambleSellection = 1
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("2x2x2", 10)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "2"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")

    
# Generation scramble and getting picture of cube 3x3x3
def cube3x3():
    global scrambleSellection
    scrambleSellection = 2
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("3x3x3", 25)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "3"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")
    

# Generation scramble and getting picture of cube 4x4x4
def cube4x4():
    global scrambleSellection
    scrambleSellection = 3
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("4x4x4", 45)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "4"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


# Generation scramble and getting picture of cube 5x5x5
def cube5x5():
    global scrambleSellection
    scrambleSellection = 4
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("5x5x5", 60)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "5"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


# Generation scramble and getting picture of cube 6x6x6
def cube6x6():
    global scrambleSellection
    scrambleSellection = 5
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("6x6x6", 85)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "6"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


# Generation scramble and getting picture of cube 7x7x7
def cube7x7():
    global scrambleSellection
    scrambleSellection = 7
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("7x7x7", 100)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        puzzle_api = "7"
        # getting picture
        loadfrom = requests.get("http://cube.rider.biz/visualcube.php?fmt=png&size=370&sch=wrgyob&pzl=" + str(puzzle_api) + "&alg=" + str(SCRAMBLE) + '"' + "&bg=t")
        image = QImage()
        image.loadFromData(loadfrom.content)
        ui.label_4.setPixmap(QPixmap(image))
        ui.label_4.show()

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


# Generation scramble without getting picture of pyraminx
def pyraminx():
    global scrambleSellection
    scrambleSellection = 6
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("pyraminx", 10)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        ui.label_4.setText(".")

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")
    

# Generation scramble without getting picture of skewb
def skewb():
    global scrambleSellection
    scrambleSellection = 8
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("skewb", 10)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        ui.label_4.setText(".")

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


# Generation scramble without getting picture of megaminx
def megaminx():
    global scrambleSellection
    scrambleSellection = 9
    url_image = 'https://google.com/'
    timeout = 10
    try:

        SCRAMBLE = sg.generate_scramble("megaminx", 77)
        SCRAMBLE.replace(" ", "")
        ui.textBrowser.setText(SCRAMBLE)
        ui.label_4.setText(".")

    except (requests.ConnectionError, requests.Timeout) as exception:
        ui.label_12.setPixmap(ui.no_internet)
        ui.textBrowser.setText("No internet connection or server is not avaible!")
        ui.label_4.setText(".")


#endless issuance of scramble after stop timer
def CallScrambleAfterStop():
    global scrambleSellection
    ui.textBrowser.setText("loading...")
    if scrambleSellection == 1:
        cube2x2()
    if scrambleSellection == 2:
        cube3x3()
    if scrambleSellection == 3:
        cube4x4()
    if scrambleSellection == 4:
        cube5x5()
    if scrambleSellection == 5:
        cube6x6()
    if scrambleSellection == 6:
        pyraminx()
    if scrambleSellection == 7:
        cube7x7()
    if scrambleSellection == 8:
        skewb()
    if scrambleSellection == 9:
        megaminx()

    
#Timer
scrambleSellection = 0
isStart = False
startTime = datetime.datetime.now()
time_delta = datetime.datetime.now()


#start function of timer
def start():
    global timer, startTime
    startTime = datetime.datetime.now()
    timer.start( 1 )
 

#stop function of timer
def stop():
    global timer
    timer.stop()

    Avg5.append(time_delta)

    Avg12.append(time_delta)
    if len(Avg5) == 5:
        average_timedelta = sum(Avg5, datetime.timedelta(0)) / len(Avg5) 
        ui.label_5.setText("ao5: " + str(average_timedelta)[:-4]) 
    if len(Avg12) == 12:
        average_timedelta_2 = sum(Avg12, datetime.timedelta(0)) / len(Avg12) 
        ui.label_6.setText("ao12: " + str(average_timedelta_2)[:-4]) 
    
    #last 5 attempt
    if len(Avg5) == 1:
        ui.label_7.setText("1." + str(Avg5[0]))
    if len(Avg5) == 2:
        ui.label_8.setText("2." + str(Avg5[1]))
    if len(Avg5) == 3:
        ui.label_9.setText("3." + str(Avg5[2]))
    if len(Avg5) == 4:
        ui.label_10.setText("4." + str(Avg5[3]))
    if len(Avg5) == 5:
        ui.label_11.setText("5." + str(Avg5[4]))
    if len(Avg5) == 6:
        Avg5.clear()
        Avg5.append(time_delta)
        reset_lables()
        ui.label_7.setText("1." + str(Avg5[0]))
        ui.label_5.setText("ao5:")
    #Update Ao12
    if len(Avg12) == 13:
        Avg12.clear()
        Avg12.append(time_delta)
        ui.label_6.setText("ao12:")
    
    #New scramble after stop function
    CallScrambleAfterStop()


#timer
def timerFunction():
    global time_delta, startTime
    time_delta = datetime.datetime.now() - startTime
    ui.lineEdit.setText(str(time_delta)[:-4] )


#Reset Lables
def reset_lables():
    ui.label_7.setText("1.")
    ui.label_8.setText("2.")
    ui.label_9.setText("3.")
    ui.label_10.setText("4.")
    ui.label_11.setText("5.")


#Reset all attempts with reset button
def ResetAttemtpsLablesAndAO5():
    reset_lables()
    Avg5.clear()
    ui.label_5.setText("ao5:")
    Avg12.clear()
    ui.label_6.setText("ao12:")


#For space bind
def OnKeyPressHandler():
    global isStart
    if isStart == False:
       start()
       isStart = True
    else:
       stop()
       isStart = False


#AO5 list
Avg5 = []


#AO12 list
Avg12 = []


#end logic
###################################




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Enigma = QtWidgets.QMainWindow()
    ui = Ui_Enigma()
    ui.setupUi(Enigma)
    Enigma.show()
    #Checking internet connection
    internet_connection()

    #Buttons
    ui.pushButton_4.clicked.connect( cube2x2 )
    ui.pushButton_6.clicked.connect( cube4x4 )
    ui.pushButton_5.clicked.connect( cube3x3 )
    ui.pushButton_7.clicked.connect( cube5x5 )
    ui.pushButton_8.clicked.connect( cube6x6 )
    ui.pushButton_9.clicked.connect( cube7x7 )
    ui.pushButton_3.clicked.connect( pyraminx )
    ui.pushButton_12.clicked.connect( megaminx )
    ui.pushButton_11.clicked.connect( skewb )
    ui.pushButton_10.clicked.connect( ResetAttemtpsLablesAndAO5 )


    #Bind
    Enigma.shortcut_open = QShortcut(QKeySequence('Space'), Enigma)
    Enigma.shortcut_open.activated.connect(OnKeyPressHandler)

    timer = QtCore.QTimer()
    timer.timeout.connect( timerFunction )

    sys.exit(app.exec_())
