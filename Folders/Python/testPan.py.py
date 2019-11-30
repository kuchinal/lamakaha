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
        #from ftrack
        shots={"shot1":["Not Started",["#L Building","#A Low Angle","#F Breath", "#P Sword","#S Medium Shot","#D West", "#C Natasha"]],"shot2":["Not Started",["#L Building","#F Breath", "#P Sword","#A Low Angle","#S Top Shot","#D West"]],"shot3":["Approved",["#L Building","#A Low Angle","#S Medium Shot","#F Steam", "#P Key","#D South", "fewfdds", "dsfdfds","fsdfefdfd","edfdd","sfgrw"]],"shot4":["In Progress",["#L Sea","#F Steam", "#P Key","#A Low Angle","#S Medium Shot","#D West", "fewfdds","#F Breath", "#P Sword", "dsfdfds","fsdfefdfd","edfdd","sfgrw"]],"shot8":["In Progress",["#L Building","#F Breath", "#P Sword","#A Low Angle","#S Medium Shot","#D West", "#C Adam"]],"shot9":["Not Started",["#L Building","#A Low Angle","#S Medium Shot","#D West", "#C Adam", "#C Natasha"]],"shot10":["Approved",["#L Building","#A Low Angle","#S Medium Shot","#D West", "#C Adam"]],"shot7":["In Progress",["#L Building","#A Low Angle","#F Steam", "#P Key","#S Medium Shot","#D West","#F Breath", "#P Sword", "#C Natasha"]],"shot21":["Not Started",["#L Building","#F Breath", "#P Sword","#A Low Angle","#S Medium Shot22","#D West", "#C Adam"]],"shot23":["Not Started",["#L Building","#A Low Angle","#S Top Shot","#D West"]],"shot34":["Approved",["#L Building","#A Low Angle","#F Steam", "#P Key","#S Medium Shot","#D South", "fewfdds","edfdd","sfgrw"]],"shot44":["In Progress",["#L Sea","#F Steam", "#P Key","#A Low Angle","#S Medium Shot","#D West", "#C Adam"]],"shot48":["Not Started",["#L Building","#A Low Angle","#S Medium Shot","#D West", "#C Adam", "#C Natasha"]],"shot49":["Not Started",["#L Building","#A Low Angle","#S Medium Shot","#D West", "#C Adam"]],"shot140":["Approved",["#L Building","#A Low Angle","#S Medium Shot","#D West"]],"shot78":["In Progress",["#L Building","#A Low Angle","#S Medium Shot","#D West"]]}
        #i am creating
        shotTags = ["#L Building","#A Low Angle","#S Medium Shot","#D West", "#C Adam","#F Breath", "#P Sword"]
        seqTags = ["#C Natasha","#L Building","#A Low Angle","#S Medium Shot","#L Corridor","#F Breath","#F Steam", "#P Key", "#P Sword","#C Adam","#D South","#D West","#S Long Shot","#C Vera","#L Kitchen","#A Eye Level","#D West","#S Close Up","#C Adam","#L Hause","#A High Angle","#L Building","#A Low Angle","#S Medium Shot","#D West", "fewfdds", "dsfdfds","fsdfefdfd","edfdd","sfgrw","#C Adam"]

        #hard coded
        statuses = ["All","Not Started","In Progress","Approved","Manual"]
        views = ["Sequence","Layout","Stack"]
        levels = ["Project","Sequence","Manual"]
        sideHeaders = ["-Status","-View","-Level"]
        sideTags = [statuses,views,levels]
        divider = ["|"]
        mainHeaders = ["_Misc","_Location","_Direction","_Character","_Prop","_FX","_Size","_Angle"]
        headers = mainHeaders+divider+sideHeaders+divider



        #remove duplicates from seqTags
        seqTags = list( dict.fromkeys(seqTags) )

        #main window settings
        self.setWindowTitle('Tagger')
        self.setMinimumWidth(1460)

        # Create the QHBoxLayout that lays out the whole form
        self.layout = QHBoxLayout()
        self.layout.setObjectName("mainLayout")

        # Create a Ok/Cancel layout
        self.ok_cancel = QVBoxLayout()
        self.ok_cancel.setObjectName("ok_cancel")
        self.ok_cancel.setAlignment(Qt.AlignBottom)

        trixIco = "/home/alexey/Dropbox/users/localRepo/Folders/Icons/bb.png"
        pixmap = QtGui.QPixmap(trixIco)
        self.picture = QtGui.Qlabel("dfdgfd")
        #   self.picture.setPixmap(pixmap)
        self.picture.setText("dfdsfds")
        self.ok_cancel.addWidget(self.picture)
        print self.picture

        #create ok and cancel buttons
        for one in ["Ok","Cancel","test"]:
            self.buttonOC = QPushButton()
            self.buttonOC.setFixedSize(70, 20)
            self.buttonOC.setCheckable(True)
            self.buttonOC.setObjectName(one)
            self.buttonOC.setText(one)
fdf
            if one == "Ok":
                Ok = self.buttonOC
                self.buttonOC.clicked.connect(lambda: okPressed(self.buttonOC))
            if one == "Cancel":
                self.buttonOC.clicked.connect(lambda: cancelPressed(self.buttonOC))            
            self.ok_cancel.addWidget(self.buttonOC)
            else:
                self.ok_cancel.addWidget(self.picture)



        #tags button
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
            self.button.clicked.connect(lambda: tagButtonClick(self,shotTags,shots,tag))

            self.button_box.addWidget(self.button)

            return self.button
        #side menu button
        def baseButton(sizeX,sizeY,tag):
            self.button = QPushButton()
            self.button.isCheckable()
            self.button.setFixedSize(sizeX, sizeY)
            self.button.setCheckable(True)
            self.button.setObjectName(tag)
            self.button.setText(tag)
        #create main tag table     
        def createColumns(headers,seqTags):

            sizeX,sizeY = 130,25
              
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
                    #self.button_box.setContentsMargins(0,0,0,0)
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
                        baseButton(sizeX,sizeY,tag)
                        self.button_box.addWidget(self.button)
                        if tag =="Approved":
                            self.button.setChecked(True)
                # add Buttons to view area
                if header == "-View":
                    for tag in views:
                        baseButton(sizeX,sizeY,tag)
                        if tag =="Layout":
                            self.button.setChecked(True)
                        self.button_box.addWidget(self.button)


                # add Buttons to level area
                if header == "-Level":
                    for tag in levels:
                        baseButton(sizeX,sizeY,tag)
                        if tag =="Sequence":
                            self.button.setChecked(True)

                        self.button_box.addWidget(self.button)

                if header == "|":
                    for one in range(5):
                        baseButton(sizeX,sizeY,tag)
                        self.button.setFixedSize(10, sizeY)
                        self.button.setText("")
                        self.button.setObjectName("")
                        self.button.setStyleSheet("background-color: black;font: bold;Text-align:center;color: white")
                        self.button_box.addWidget(self.button)               



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
                collector(self)
                self.close()
        def cancelPressed(button):
                print 'cancel pressed'
                self.close()

        #iterate trough objects in layouts
        def layout_widgets(layout):
           return (layout.itemAt(i) for i in range(layout.count()))


 
        #iterate over all buttons
        def collector(self):
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
            print pressedTags
            print status
            print view
            print level
            return pressedTags
            return status 
            return view
            return level

        def tagButtonClick(self,shotTags,shots,tag):
            shotTags = collector(self)
            #check collection of the combinations
            ip,ns,ap = 0,0,0
            for one in shots:
                found = 1
                for sone in shotTags:
                    if sone not in shots[one][1]:
                        found = 0
                if found == 1:
                    if shots[one][0] == "In Progress":
                        ip= ip +1
                    if shots[one][0] == "Not Started":
                        ns= ns +1
                    if shots[one][0] == "Approved":
                        ap= ap +1


            #find Status buttons and add them numbers
            for w in layout_widgets(self.layout):
                wName =  w.objectName() #layout name
                #collect all pressed buttons
                if wName == "Status":
                    for i in range(w.count()):
                        myWidget = w.itemAt(i).widget()
                        name = myWidget.objectName()
                        import re
                        t = re.sub(r'\s[0-9]+', '', myWidget.text())+" "
                        if name =="Not Started":
                            myWidget.setText(t+str(ns))

                        if name =="In Progress":
                            myWidget.setText(t+str(ip))

                        if name =="Approved":
                            self.button.setChecked(True)
                            myWidget.setText(t+str(ap))
                # elif wName in ["View","Angle"]:
                #     for i in range(w.count()):
                #         myWidget = w.itemAt(i).widget()
                #         myWidget.setChecked(False)
                #         if myWidget.text()== tag:
                #             myWidget.setChecked(True)
                 
        #run collect on the startup
        tagButtonClick(self,shotTags,shots,self.button)




        # def mousePressEvent(self, QMouseEvent):
        #     #print mouse position
        #     #print QMouseEvent.source()
        #     print 'click!!!!'

        # mousePressEvent(self, QMouseEvent)

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