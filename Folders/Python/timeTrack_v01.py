import sys
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import re
from datetime import date
from functools import partial
from PySide.QtCore import Qt




workedShots = {"DKC_TST_0010_comp":[1.3,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.01.png"],"DKC_TST_0020_comp":[2.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.05.png"],"DKC_TST_0030_comp":[2,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.02.png"],"DKC_TST_0040_comp":[1.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TST_0040_prep":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.04.png"]}

class timeTrack(QFrame):

    ''' An example of PySide absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''
 
    def __init__(self):
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QFrame.__init__(self)


        sizeX = 50
        sizeY = 50

        #add border to the panel
        self.setLineWidth(3)
        self.setFrameStyle(QFrame.Box|QFrame.Sunken)


        

        #add some icon
        trixIco = "/mnt/Hobby/projects/TAG/07_Masters/baby.png"
        pixmap = QPixmap(trixIco)
        self.picture = QLabel()
        self.picture.setPixmap(pixmap)
        self.picture.setScaledContents(True)
        self.picture.setFixedSize(70, 70)




        #main window settings
        self.setWindowTitle('time track')
        self.setMinimumWidth(1460)

        # Create the QGridLayout that lays out the whole form
        self.grid = QGridLayout()
        self.grid.setObjectName("mainGrid")
        self.setLayout(self.grid)

        # add Date and time stamp
        curTime = str(date.today())
        self.time = QLabel()
        self.time.setText(curTime)
        self.time.setScaledContents(True)
        #self.time.setFixedSize(170, 70) 
        self.time.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
 

        # add Hours represention button
        self.hours = QLabel()
        self.hours.setText("0")

        self.hours.setScaledContents(True)
        self.hours.setFixedSize(100, 100)  
        self.hours.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")


        #joke button
        trixIco = "/mnt/Hobby/projects/TimeTrack/04_Elements/R.jpeg"
        pixJoke = QPixmap(trixIco)
        self.joke = QPushButton()
        self.joke.setIcon(pixJoke)
        self.joke.setIconSize(pixmap.rect().size())
        #self.joke.setScaledContents(True)
        #self.joke.setFixedSize(200, 200)
        self.joke.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
        self.joke.clicked.connect(lambda: okPressed())
        #iterate trough objects in layouts
        def layout_widgets(layout):
           return (layout.itemAt(i) for i in range(layout.count()))


        def collectHours():
           #collect all combined hours
            finalResult = {}
            summ = 0
            for w in layout_widgets(self.shotsLayout):
                wName =  w.objectName() #layout name
                for i in range(w.count()):
                    myWidget = w.itemAt(i).widget()
                    name = myWidget.objectName()
                    if "hourEntry" in name:
                        pName = re.findall("\|.+\|",name)[0].replace("|","")
                        finalResult[pName] = myWidget.text()
                        summ = float(myWidget.text())+summ
            self.hours.setText(str(summ))
            print finalResult

        def setHour(entry,result,sL):

            # update hour count in for shot
            entry.setText(result)
            #get numbers buttons and 
            numbers = []
            for one in range(13):
                d = sL.itemAt(one).widget()
                if "hourButton" in d.objectName():
                    numbers.append(d)

            #check button
            for w in numbers:
                w.setChecked(False)
            for w in numbers:
                if w.objectName()[0] == result:
                    w.setChecked(True)

            collectHours()



        # Create hours layout and populate it
        def shotLayout(shotName,Hours,thumbnail):
            pressed = 0
            #set font
            font = QFont()
            font.setPointSize(50)
            font.setWeight(75)
            font.setItalic(False)
            font.setBold(True)

            self.shotLayout = QHBoxLayout()
            self.shotLayout.setObjectName(shotName)
            sL = self.shotLayout
            self.shotLayout.setAlignment(Qt.AlignTop)

            #add thumbnail
            pixmap = QPixmap(thumbnail)
            self.picture = QLabel()
            self.picture.setPixmap(pixmap)
            self.picture.setScaledContents(True)
            self.picture.setFixedSize(130, 70)
            self.picture.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
            self.shotLayout.addWidget(self.picture)

            #add shot name
            self.shotN = QLabel()
            self.shotN.setText(shotName)
            self.shotN.setFixedSize(400, 70)
            self.shotN.setScaledContents(True)

            self.shotN.setStyleSheet("font: bold 25px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
            self.shotLayout.addWidget(self.shotN)

            #add manual entry for hours
            self.mEntry = QLineEdit()
            self.mEntry.setText(str(Hours))
            self.mEntry.setObjectName(str(Hours)+"|"+shotName+"|hourEntry")
            self.mEntry.setFixedSize(100, 70)
            self.mEntry.setStyleSheet("font: bold 40px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
            self.mEntry.textChanged.connect(lambda : collectHours())
            self.shotLayout.addWidget(self.mEntry)
            #add hours
            for hour in range(10):
                self.hour = QPushButton()
                self.hour.isCheckable()
                self.hour.setFixedSize(55, 70)
                self.hour.setFont(font)
                self.hour.setCheckable(True)
                self.hour.setObjectName(str(hour)+"|"+shotName+"|hourButton")
                self.hour.setText(str(hour))
                self.hour.setFocusPolicy(QtCore.Qt.NoFocus)
                txt = self.hour.text()
                if txt == str(int(Hours)):
                    self.hour.setChecked(True)
                self.hour.clicked.connect(partial(setHour, self.mEntry,txt,sL))
                self.shotLayout.addWidget(self.hour)


        # Create shots layout
        self.shotsLayout = QVBoxLayout()
        self.shotsLayout.setObjectName("all shots")
        self.shotsLayout.setAlignment(Qt.AlignTop)


        count = 0
        for one in workedShots:
            shotLayout(shotName=one,Hours=workedShots[one][0],thumbnail = workedShots[one][1])
            self.shotsLayout.addLayout(self.shotLayout,count)
            count = count+1
            

        #add layouts to grid
        self.grid.addLayout(self.shotsLayout,1,0)
        self.grid.addWidget(self.time,0,0)
        self.grid.addWidget(self.hours,0,1)
        self.grid.addWidget(self.joke,1,1)
        collectHours()


        def okPressed():
                collectHours()
                self.close()



    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        #qt_app.exec_()
 
# Create an instance of the application window and run it
app = timeTrack()
app.run()


#in nuke:
# import testPan
# reload(testPan)