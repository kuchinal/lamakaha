import sys
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import re
from datetime import date
from functools import partial
from PySide.QtCore import Qt





jokeIco = "/mnt/Hobby/projects/TimeTrack/03_Data/progress."
trixIco = "/mnt/Hobby/projects/TAG/07_Masters/baby.png"

workedShots = {"DKC_TST_0010_comp":[0.3,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.01.png"],"DKC_TST_0020_comp":[1.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.05.png"],"DKC_TST_0030_comp":[1,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.02.png"],"DKC_TST_0040_comp":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TST_0040_prep":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.04.png"]}

def getShots(date):
    if date == "22/11/19":
        workedShots = {"DKC_TST_0010_paint":[0.3,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.01.png"],"DKC_TST_0020_comp":[1.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.05.png"],"DKC_TST_0074_prep":[1,"/mnt/Hobby/projects/TimeTrack/02_Data/thumbnail.01.png"],"DKC_TST_0040_comp":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TST_0350_prep":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.04.png"],"DKC_TET_4550_prep":[0.2,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.01.png"]}
    elif date == "29/11/19":
        workedShots = {"DKC_TST_0010_comp":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.02.png"],"DKC_TST_0020_comp":[1.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TST_1130_paint":[3,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.01.png"],"DKC_TST_0040_comp":[0.2,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.04.png"],"DKC_TST_0080_prep":[4.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.04.png"]}
    elif date == "15/11/19":
        workedShots = {"DKC_TST_0010_comp":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.07.png"],"DKC_TST_0010_comp":[0.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.06.png"],"DKC_TST_0020_comp":[1.5,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TST_0130_comp":[3,"/mnt/Hobby/projects/TimeTrack/06_Data/thumbnail.07.png"],"DKC_TST_0040_comp":[0.2,"/mnt/Hobby/projects/TimeTrack/03_Data/thumbnail.03.png"],"DKC_TRT_0080_prep":[4.5,"/mnt/Hobby/projects/TimeTrack/05_Data/thumbnail.04.png"]}

    return workedShots

class timeTrack(QFrame):

    ''' An example of PySide absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''
 
    def __init__(self):
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QFrame.__init__(self)


        sizeX = 50
        sizeY = 50
        hourButtonWidth = 80
        #add border to the panel
        self.setLineWidth(3)
        self.setFrameStyle(QFrame.Box|QFrame.Sunken)



        #add some icon
        
        pixmap = QPixmap(trixIco)
        self.picture = QLabel()
        self.picture.setPixmap(pixmap)
        self.picture.setScaledContents(True)
        self.picture.setFixedSize(70, 70)


        #main window settings
        self.setWindowTitle('Task Master')
        self.setMinimumWidth(1900)

        # Create the QGridLayout that lays out the whole form
        self.grid = QGridLayout()
        self.grid.setObjectName("mainGrid")
        self.setLayout(self.grid)

        #add calendar
        self.calendar = QCalendarWidget()
        self.calendar.setFirstDayOfWeek(Qt.Monday)

        self.calendar.setFixedSize(800, 150)



        # add Hours represention button
        self.hours = QLabel()
        self.hours.setText("0")
        self.hours.setScaledContents(True)
        self.hours.setFixedSize(100, 100)  
        self.hours.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")


        #joke button

        pix = jokeIco+"01.png"

        pixJoke = QPixmap(pix)
        self.joke = QPushButton()
        self.joke.setIcon(pixJoke)
        self.joke.setIconSize(pixmap.rect().size())
        self.joke.setStyleSheet("font: bold 34px;Text-align:center;color: white;border-style: outset;border-width: 2px;border-color: beige;")
        self.joke.clicked.connect(lambda: okPressed())



        def clearLayout(layout):
                if layout is not None:
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            clearLayout(item.layout())


        def showDate(date):
            clearLayout(self.shotsLayout)

            getDate =  date.toString("dd/MM/yy")
            workedShots = getShots(getDate)
            buildUI(workedShots)
            return workedShots





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

            #set funny picture
            if summ<=10:
                pix = jokeIco+str("%02d" % round(summ))+".png"
            else:
                pix = "/mnt/Hobby/projects/TimeTrack/04_Elements/R.jpeg"
            pixJoke = QPixmap(pix)
            self.joke.setIcon(pixJoke)
            #print finalResult

        def setHour(entry,result,sL):


            #get numbers buttons and 
            numbers = []
            for one in range(12):
                d = sL.itemAt(one).widget()
                if "hourButton" in d.objectName():
                    numbers.append(d)


            cur = ""
            for w in numbers:
                if w.isChecked():
                    cur = w.objectName()[0]

            #check button
            for w in numbers:
                w.setChecked(False)
            for w in numbers:
                if w.objectName()[0] == result:
                    w.setChecked(True)
 
                    if not cur:
                        pos = QCursor().pos().x()

                        bPos =  w.parentWidget().mapToGlobal( w.pos() ).x()
                        center = bPos+hourButtonWidth/2

                        if pos > center:
                            r =str(float(entry.text())+0.1)
                        else:
                            r =str(float(entry.text())-0.1)
                        entry.setText(r)
                    else:
                        entry.setText(result)




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
            for hour in range(9):
                self.hour = QPushButton()
                self.hour.isCheckable()
                self.hour.setFixedSize(hourButtonWidth, 70)
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


        def buildUI(workedShots):
            # Create shots layout
            self.shotsLayout = QVBoxLayout()
            self.shotsLayout.setObjectName("all shots")
            self.shotsLayout.setAlignment(Qt.AlignTop)

            count = 0
            for one in workedShots:
                print one
                shotLayout(shotName=one,Hours=workedShots[one][0],thumbnail = workedShots[one][1])
                self.shotsLayout.addLayout(self.shotLayout,count)
                count = count+1

            #add layouts to grid
            self.grid.addLayout(self.shotsLayout,1,0)

            self.grid.addWidget(self.calendar,0,0)
            self.grid.addWidget(self.hours,0,1)
            self.grid.addWidget(self.joke,1,1)
            collectHours()

        buildUI(workedShots)

        def okPressed():
                collectHours()
                self.close()

        self.calendar.clicked[QtCore.QDate].connect(showDate)


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