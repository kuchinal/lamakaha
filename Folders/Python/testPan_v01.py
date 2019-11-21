import sys
from PySide.QtCore import *
from PySide.QtGui import *
import re
# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
#qt_app = QApplication(sys.argv)
 
class TagGroups(QWidget):

    ''' An example of PySide absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''
 
    def __init__(self):
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QWidget.__init__(self)

        #variables
        shots={"shot1":["Not Started",["#L Building","#A Low Angle","#S Medium Shot","#D West"]],"shot2":["Not Started",["#L Building","#A Low Angle","#S Medium Shot","#D West"]]}
        shotTags = ["#L Building","#A Low Angle","#S Medium Shot","#D West", "fewfdds", "dsfdfds","fsdfefdfd","edfdd","sfgrw","#C Adam"]
        seqTags = ["#L Building","#A Low Angle","#S Medium Shot","#L Corridor","#C Adam","#D South","#D West","#S Long Shot","#C Vera","#L Kitchen","#A Eye Level","#D West","#S Close Up","#C Natasha","#L Hause","#A High Angle","#L Building","#A Low Angle","#S Medium Shot","#D West", "fewfdds", "dsfdfds","fsdfefdfd","edfdd","sfgrw","#C Adam"]


        statuses = ["All","Not Started","In Progress","Approved","Manual"]
        views = ["Sequence.","Layout.","Stack."]
        levels = ["Project","Sequence","Manual"]
        sideHeaders = ["-Status","-View","-Level"]
        sideTags = [statuses,views,levels]
        divider = ["|"]
        mainHeaders = ["_Misc","_Location","_Direction","_Character","_Size","_Angle"]
        headers = mainHeaders+divider+sideHeaders



        #remove duplicates from seqTags
        seqTags = list( dict.fromkeys(seqTags) )

        #main window settings
        self.setWindowTitle('Tagger')
        self.setMinimumWidth(1200)

        # Create the QHBoxLayout that lays out the whole form
        self.layout = QHBoxLayout()
        self.layout.setObjectName("mainLayout")

        # Create a Ok/Cancel layout
        self.ok_cancel = QVBoxLayout()
        self.ok_cancel.setObjectName("ok_cancel")
        self.ok_cancel.setAlignment(Qt.AlignBottom)

        #create ok and cancel buttons
        for one in ["Ok","Cancel"]:
            self.buttonOC = QPushButton()
            self.buttonOC.setFixedSize(70, 20)
            self.buttonOC.setCheckable(True)
            self.buttonOC.setObjectName(one)
            self.buttonOC.setText(one)
            if one == "Ok":
                Ok = self.buttonOC
                self.buttonOC.clicked.connect(lambda: okPressed(self.buttonOC))
            if one == "Cancel":
                self.buttonOC.clicked.connect(lambda: cancelPressed(self.buttonOC))            
            self.ok_cancel.addWidget(self.buttonOC)

        #basic button
        def mkButton(sizeX,sizeY,tag, pat=""):
            self.button = QPushButton()
            self.button.isCheckable()
            self.button.setFixedSize(sizeX, sizeY)
            self.button.setCheckable(True)
            if tag in shotTags:
                self.button.setChecked(True)
            self.button.setObjectName(tag)
            tag = tag.replace(pat,'').replace("#",'')
            self.button.setText(tag)

            self.button_box.addWidget(self.button)

            if tag in ["Approved","Layout.","Sequence"]:
                self.button.setChecked(True)
            return self.button

        #create main tag table     
        def createColumns(headers,seqTags):

            sizeX = 130
            sizeY = 25
            for header in headers:
                pat = "#"+header.replace("_","")[0]
                # Create a vertical box layout
                self.button_box = QVBoxLayout()
                self.button_box.setObjectName(header[1:])
                self.button_box.setAlignment(Qt.AlignTop)
                
                # add header to the collumn
                self.label = QPushButton()
                self.label.setText(header[1:])
                self.label.setObjectName(header[1:])
                self.label.setStyleSheet("background-color: black;font: bold;Text-align:center;color: white")
                self.label.setFixedSize(sizeX, sizeY)
                if header == "|":
                    self.label.setFixedSize(10, sizeY)

                self.button_box.addWidget(self.label)

                # add Buttons to tagged area
                for tag in seqTags:
                    if pat in tag: 
                        mkButton( sizeX, sizeY, tag, pat)

                # add Buttons to Misc area
                if header == "_Misc":
                    for tag in seqTags:
                        if "#" not in tag: 
                            mkButton( sizeX, sizeY, tag, pat).setChecked(False)

                # add Buttons to status area
                if header == "-Status":
                    for tag in statuses:
                        mkButton(sizeX,sizeY,tag)

                # add Buttons to view area
                if header == "-View":
                    for tag in views:
                        mkButton(sizeX,sizeY,tag)


                # add Buttons to level area
                if header == "-Level":
                    for tag in levels:
                        mkButton(sizeX,sizeY,tag)



                # Add the button box to the  the main layout
                self.layout.addLayout(self.button_box,headers.index(header))

        #create main columns
        createColumns(headers,seqTags)

        # add ok_cancel layout
        self.layout.addLayout(self.ok_cancel,11)

        # Set the VBox layout as the window's main layout
        self.setLayout(self.layout)

        ###############################################################

        def okPressed(button):
                collector()
                self.close()
        def cancelPressed(button):
                print 'cancel pressed'
                self.close()

        #iterate trough objects in layouts
        def layout_widgets(layout):
           return (layout.itemAt(i) for i in range(layout.count()))


 
        #iterate over all buttons
        def collector():
            pressedTags = []
            status = []
            view = []
            level = []
            for w in layout_widgets(self.layout):
                wName =  w.objectName() #layout name

                #collect all pressed buttons
                if "_"+wName in mainHeaders:
                    for i in range(w.count()):
                        myWidget = w.itemAt(i).widget()
                        name = myWidget.objectName()
                        if myWidget.isChecked():
                            pressedTags.append(name)

                elif wName in "Status":
                    for i in range(w.count()):
                        myWidget = w.itemAt(i).widget()
                        name = myWidget.objectName()
                        if myWidget.isChecked():
                            status.append(name)
                elif wName in "View":
                    for i in range(w.count()):
                        myWidget = w.itemAt(i).widget()
                        name = myWidget.objectName()
                        if myWidget.isChecked():
                            view.append(name.replace(".",""))
                elif wName in "Level":
                    for i in range(w.count()):
                        myWidget = w.itemAt(i).widget()
                        name = myWidget.objectName()
                        if myWidget.isChecked():
                            level.append(name)
            return pressedTags
            return status 
            return view
            return level

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        #qt_app.exec_()
 
# Create an instance of the application window and run it
app = TagGroups()
app.run()


#in nuke:
# import testPan
# reload(testPan)