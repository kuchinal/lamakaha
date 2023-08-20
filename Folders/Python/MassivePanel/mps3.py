import nuke
import nukescripts
from nukescripts import panels
import random
import time
import sys # We need sys so that we can pass argv to QApplication
import os






if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtUiTools, QtGui as QtWidgets
    from PySide.QtCore import Qt
    from PySide.QtGui import QCompleter
    
else:
    from PySide2 import QtGui, QtUiTools, QtCore, QtWidgets# Import the PyQt4 module we'll need
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QCompleter



def killPaneMargins(widget_object):
    if widget_object:
        target_widgets = set()
        target_widgets.add(widget_object.parentWidget().parentWidget())
        target_widgets.add(widget_object.parentWidget().parentWidget().parentWidget().parentWidget())

        for widget_layout in target_widgets:
            try:
                widget_layout.layout().setContentsMargins(0, 0, 0, 0)
            except:
                pass



def _read_ui(parent=None):
        loader = QtUiTools.QUiLoader()
        thisFileDir = os.path.dirname(os.path.realpath(__file__))
        ui_file = QtCore.QFile(thisFileDir+"/Massive_v02.ui") #path to .ui file
        #ui_file = QtCore.QFile( "/home/lamakaha/.nuke/Mdev/Massive.ui") #path to .ui file
        ui_file.open(QtCore.QFile.ReadOnly)
        mdev_file = loader.load(ui_file, parent)# here i tried to just assign the ui_file to mdev
        ui_file.close()
        return mdev_file

#here i am starting to get problems
#
class MassivePanelPySide(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(MassivePanelPySide, self).__init__(parent)
        self.ui = _read_ui(self)



        #class MassivePanelPySide(QtGui.QMainWindow, mdev.Ui_widget):

        # class MassivePanelPySide(QtGui.QMainWindow, mdev.Ui_widget):
        #     def __init__(self):
        #         super(self.__class__, self).__init__()
        #         self.setupUi(self) 




        ####### connecting buttons

        #assign takes to selected nodes
        self.ui.take1.clicked.connect(lambda: self.setTake(self.ui.take1,self.ui.resetTake1,self.ui.disableTake1,self.ui.take1Low,self.ui.take1High,self.ui.selectTake1,self.ui.icons))
        self.ui.take2.clicked.connect(lambda: self.setTake(self.ui.take2,self.ui.resetTake2,self.ui.disableTake2,self.ui.take2Low,self.ui.take2High,self.ui.selectTake2,self.ui.icons))
        self.ui.take3.clicked.connect(lambda: self.setTake(self.ui.take3,self.ui.resetTake3,self.ui.disableTake3,self.ui.take3Low,self.ui.take3High,self.ui.selectTake3,self.ui.icons))
        self.ui.take4.clicked.connect(lambda: self.setTake(self.ui.take4,self.ui.resetTake4,self.ui.disableTake4,self.ui.take4Low,self.ui.take4High,self.ui.selectTake4,self.ui.icons))
        self.ui.take5.clicked.connect(lambda: self.setTake(self.ui.take5,self.ui.resetTake5,self.ui.disableTake5,self.ui.take5Low,self.ui.take5High,self.ui.selectTake5,self.ui.icons))
        self.ui.take6.clicked.connect(lambda: self.setTake(self.ui.take6,self.ui.resetTake6,self.ui.disableTake6,self.ui.take6Low,self.ui.take6High,self.ui.selectTake6,self.ui.icons))
        self.ui.take7.clicked.connect(lambda: self.setTake(self.ui.take7,self.ui.resetTake7,self.ui.disableTake7,self.ui.take7Low,self.ui.take7High,self.ui.selectTake7,self.ui.icons))
        self.ui.take8.clicked.connect(lambda: self.setTake(self.ui.take8,self.ui.resetTake8,self.ui.disableTake8,self.ui.take8Low,self.ui.take8High,self.ui.selectTake8,self.ui.icons))
        self.ui.take9.clicked.connect(lambda: self.setTake(self.ui.take9,self.ui.resetTake9,self.ui.disableTake9,self.ui.take9Low,self.ui.take9High,self.ui.selectTake9,self.ui.icons))
        self.ui.take10.clicked.connect(lambda: self.setTake(self.ui.take10,self.ui.resetTake10,self.ui.disableTake10,self.ui.take10Low,self.ui.take10High,self.ui.selectTake10,self.ui.icons))
        self.ui.take11.clicked.connect(lambda: self.setTake(self.ui.take11,self.ui.resetTake11,self.ui.disableTake11,self.ui.take11Low,self.ui.take11High,self.ui.selectTake11,self.ui.icons))

        #connecting select takes
        self.ui.selectTake1.clicked.connect(lambda: self.selectTake(self.ui.take1,self.ui.resetTake1,self.ui.disableTake1,self.ui.take1Low,self.ui.take1High,self.ui.selectTake1))
        self.ui.selectTake2.clicked.connect(lambda: self.selectTake(self.ui.take2,self.ui.resetTake2,self.ui.disableTake2,self.ui.take2Low,self.ui.take2High,self.ui.selectTake2))
        self.ui.selectTake3.clicked.connect(lambda: self.selectTake(self.ui.take3,self.ui.resetTake3,self.ui.disableTake3,self.ui.take3Low,self.ui.take3High,self.ui.selectTake3))
        self.ui.selectTake4.clicked.connect(lambda: self.selectTake(self.ui.take4,self.ui.resetTake4,self.ui.disableTake4,self.ui.take4Low,self.ui.take4High,self.ui.selectTake4))
        self.ui.selectTake5.clicked.connect(lambda: self.selectTake(self.ui.take5,self.ui.resetTake5,self.ui.disableTake5,self.ui.take5Low,self.ui.take5High,self.ui.selectTake5))
        self.ui.selectTake6.clicked.connect(lambda: self.selectTake(self.ui.take6,self.ui.resetTake6,self.ui.disableTake6,self.ui.take6Low,self.ui.take6High,self.ui.selectTake6))
        self.ui.selectTake7.clicked.connect(lambda: self.selectTake(self.ui.take7,self.ui.resetTake7,self.ui.disableTake7,self.ui.take7Low,self.ui.take7High,self.ui.selectTake7))
        self.ui.selectTake8.clicked.connect(lambda: self.selectTake(self.ui.take8,self.ui.resetTake8,self.ui.disableTake8,self.ui.take8Low,self.ui.take8High,self.ui.selectTake8))
        self.ui.selectTake9.clicked.connect(lambda: self.selectTake(self.ui.take9,self.ui.resetTake9,self.ui.disableTake9,self.ui.take9Low,self.ui.take9High,self.ui.selectTake9))
        self.ui.selectTake10.clicked.connect(lambda: self.selectTake(self.ui.take10,self.ui.resetTake10,self.ui.disableTake10,self.ui.take10Low,self.ui.take10High,self.ui.selectTake10))
        self.ui.selectTake11.clicked.connect(lambda: self.selectTake(self.ui.take11,self.ui.resetTake11,self.ui.disableTake11,self.ui.take11Low,self.ui.take11High,self.ui.selectTake11))

        #connecting disable/toggle takes
        self.ui.disableTake1.clicked.connect(lambda: self.disableTake(self.ui.take1,self.ui.resetTake1,self.ui.disableTake1,self.ui.take1Low,self.ui.take1High,self.ui.selectTake1,self.ui.icons))
        self.ui.disableTake2.clicked.connect(lambda: self.disableTake(self.ui.take2,self.ui.resetTake2,self.ui.disableTake2,self.ui.take2Low,self.ui.take2High,self.ui.selectTake2,self.ui.icons))
        self.ui.disableTake3.clicked.connect(lambda: self.disableTake(self.ui.take3,self.ui.resetTake3,self.ui.disableTake3,self.ui.take3Low,self.ui.take3High,self.ui.selectTake3,self.ui.icons))
        self.ui.disableTake4.clicked.connect(lambda: self.disableTake(self.ui.take4,self.ui.resetTake4,self.ui.disableTake4,self.ui.take4Low,self.ui.take4High,self.ui.selectTake4,self.ui.icons))
        self.ui.disableTake5.clicked.connect(lambda: self.disableTake(self.ui.take5,self.ui.resetTake5,self.ui.disableTake5,self.ui.take5Low,self.ui.take5High,self.ui.selectTake5,self.ui.icons))
        self.ui.disableTake6.clicked.connect(lambda: self.disableTake(self.ui.take6,self.ui.resetTake6,self.ui.disableTake6,self.ui.take6Low,self.ui.take6High,self.ui.selectTake6,self.ui.icons))
        self.ui.disableTake7.clicked.connect(lambda: self.disableTake(self.ui.take7,self.ui.resetTake7,self.ui.disableTake7,self.ui.take7Low,self.ui.take7High,self.ui.selectTake7,self.ui.icons))
        self.ui.disableTake8.clicked.connect(lambda: self.disableTake(self.ui.take8,self.ui.resetTake8,self.ui.disableTake8,self.ui.take8Low,self.ui.take8High,self.ui.selectTake8,self.ui.icons))
        self.ui.disableTake9.clicked.connect(lambda: self.disableTake(self.ui.take9,self.ui.resetTake9,self.ui.disableTake9,self.ui.take9Low,self.ui.take9High,self.ui.selectTake9,self.ui.icons))
        self.ui.disableTake10.clicked.connect(lambda: self.disableTake(self.ui.take10,self.ui.resetTake10,self.ui.disableTake10,self.ui.take10Low,self.ui.take10High,self.ui.selectTake10,self.ui.icons))
        self.ui.disableTake11.clicked.connect(lambda: self.disableTake(self.ui.take11,self.ui.resetTake11,self.ui.disableTake11,self.ui.take11Low,self.ui.take11High,self.ui.selectTake11,self.ui.icons))

        #connecting reset takes
        self.ui.resetTake1.clicked.connect(lambda: self.resetTake(self.ui.take1,self.ui.resetTake1,self.ui.disableTake1,self.ui.take1Low,self.ui.take1High,self.ui.selectTake1))
        self.ui.resetTake2.clicked.connect(lambda: self.resetTake(self.ui.take2,self.ui.resetTake2,self.ui.disableTake2,self.ui.take2Low,self.ui.take2High,self.ui.selectTake2))
        self.ui.resetTake3.clicked.connect(lambda: self.resetTake(self.ui.take3,self.ui.resetTake3,self.ui.disableTake3,self.ui.take3Low,self.ui.take3High,self.ui.selectTake3))
        self.ui.resetTake4.clicked.connect(lambda: self.resetTake(self.ui.take4,self.ui.resetTake4,self.ui.disableTake4,self.ui.take4Low,self.ui.take4High,self.ui.selectTake4))
        self.ui.resetTake5.clicked.connect(lambda: self.resetTake(self.ui.take5,self.ui.resetTake5,self.ui.disableTake5,self.ui.take5Low,self.ui.take5High,self.ui.selectTake5))
        self.ui.resetTake6.clicked.connect(lambda: self.resetTake(self.ui.take6,self.ui.resetTake6,self.ui.disableTake6,self.ui.take6Low,self.ui.take6High,self.ui.selectTake6))
        self.ui.resetTake7.clicked.connect(lambda: self.resetTake(self.ui.take7,self.ui.resetTake7,self.ui.disableTake7,self.ui.take7Low,self.ui.take7High,self.ui.selectTake7))
        self.ui.resetTake8.clicked.connect(lambda: self.resetTake(self.ui.take8,self.ui.resetTake8,self.ui.disableTake8,self.ui.take8Low,self.ui.take8High,self.ui.selectTake8))
        self.ui.resetTake9.clicked.connect(lambda: self.resetTake(self.ui.take9,self.ui.resetTake9,self.ui.disableTake9,self.ui.take9Low,self.ui.take9High,self.ui.selectTake9))
        self.ui.resetTake10.clicked.connect(lambda: self.resetTake(self.ui.take10,self.ui.resetTake10,self.ui.disableTake10,self.ui.take10Low,self.ui.take10High,self.ui.selectTake10))
        self.ui.resetTake11.clicked.connect(lambda: self.resetTake(self.ui.take11,self.ui.resetTake11,self.ui.disableTake11,self.ui.take11Low,self.ui.take11High,self.ui.selectTake11))

        #refresh takes
        self.ui.refresh.clicked.connect(self.refreshTakes)

        #toggle mb in rotos and rotoshapes
        self.ui.rotosMB.clicked.connect(lambda: self.rotosMBtoggle(self.ui.rotosMB,self.ui.icons))

        #connecting Go button
        self.ui.go.clicked.connect(lambda: self.goGo(self.ui.go,self.ui.knob,self.ui.value,self.ui.increment,self.ui.red,self.ui.green,self.ui.blue,self.ui.alpha,self.ui.kind,self.ui.arithmetic,self.ui.geometric))
        
        self.ui.rreplace.setToolTip("replace with this string, \n\ntrick you can use - if you want to set the version for the Read node \nyou can just leave the 'search' field empty \nand type the desired version number in the 'replace' field, press 'Replace' and version will be set!")
        #connecting search and replace
        #self.ui.find.returnPressed.connect(lambda: self.searchAndReplace(self.ui.find,self.ui.replace,self.ui.knob))
        #self.ui.replace.returnPressed.connect(lambda: self.searchAndReplace(self.ui.find,self.ui.replace,self.ui.knob))
        self.ui.replaceIt.clicked.connect(lambda: self.searchAndReplace(self.ui.ffind,self.ui.rreplace,self.ui.knob))


        # nodegraph nodes manipulation
        self.ui.up.clicked.connect(lambda: self.scaleNodes( 1,1.3))
        self.ui.down.clicked.connect(lambda: self.scaleNodes(  1, .7 ))
        self.ui.left.clicked.connect(lambda: self.scaleNodes( .7, 1 ))
        self.ui.right.clicked.connect(lambda: self.scaleNodes( 1.3, 1 ))
        self.ui.alignNodesHorizontally.clicked.connect( lambda: self.alignNodes(nuke.selectedNodes(), direction="y"))
        self.ui.alignNodesVertically.clicked.connect( lambda: self.alignNodes(nuke.selectedNodes(), direction="x"))
        self.ui.checkerboardNodes.clicked.connect( lambda: self.checkerboardNodesAll())


        #setting or removing animations
        self.ui.setAnimated.clicked.connect(lambda: self.setAnimatedNodes(self.ui.knob))
        self.ui.clearAnimated.clicked.connect(lambda: self.clearAnimatedNodes(self.ui.knob))

        # setting icons button 
        self.ui.icons.setCheckable(1)
        self.ui.icons.clicked.connect(lambda: self.killIcons(self.ui.icons))


        #defining focus events
        self.ui.knob.returnPressed.connect(lambda : self.focusEvent(self.ui.knob))
        self.ui.value.returnPressed.connect(lambda : self.focusEvent(self.ui.value))
        self.ui.increment.returnPressed.connect(lambda : self.focusEvent(self.ui.increment))
        #self.ui.find.returnPressed.connect(lambda : self.focusEvent(self.ui.find))
        #self.ui.replace.returnPressed.connect(lambda : self.focusEvent(self.ui.replace))
        self.ui.knob.textChanged.connect(lambda : self.gotFocusEvent(self.ui.knob))
        self.ui.errorMessage = "please send this error to Alexey so he will be able to uncrap his code \n\n\n but before you are doing that please tripple check that you are trying to set legit values and not some senseless crap\n\n\n thank you."

        # connect memory to setting values to knobs 
        self.ui.memory.activated.connect(lambda : self.setMemory(self.ui.memory))
        #connect change of kind to memory grab
        self.ui.grabMemo.clicked.connect(lambda : self.grabMemory(self.ui.kind, self.ui.memory))
        #store entered values in the memoryau
        self.ui.go.clicked.connect(lambda: self.massiveMemory(self.ui.knob,self.ui.value,self.ui.increment,self.ui.red,self.ui.green,self.ui.blue,self.ui.alpha,self.ui.kind))


        self.ui.redB.clicked.connect(lambda: self.setNodesColor(2466250752L))
        self.ui.greenB.clicked.connect(lambda: self.setNodesColor(1063467008L))
        self.ui.blueB.clicked.connect(lambda: self.setNodesColor(1027575296L))
        self.ui.magentaB.clicked.connect(lambda: self.setNodesColor(1358974720L))
        self.ui.cyanB.clicked.connect(lambda: self.setNodesColor(16777215))
        self.ui.yellowB.clicked.connect(lambda: self.setNodesColor(2526413055))
        self.ui.whiteB.clicked.connect(lambda: self.setNodesColor(4294967040))
        self.ui.blackB.clicked.connect(lambda: self.setNodesColor(255))
        self.ui.grayB.clicked.connect(lambda: self.setNodesColor(2139062271))
        self.ui.resetColor.clicked.connect(lambda: self.setNodesColor(0))


        self.ui.Rconnect.clicked.connect(lambda: self.randomConnectNodes())


        self.ui.snap3D.clicked.connect(lambda: self.snap3Dgeo())

        self.ui.reloadReads.clicked.connect(lambda: self.readsReload())
        
        self.ui.countSelected.clicked.connect(lambda: self.countSelectedNodes())

        self.ui.arithmetic.clicked.connect(lambda: self.incrProgressA(self.ui.arithmetic,self.ui.geometric))
        self.ui.geometric.clicked.connect(lambda: self.incrProgressG(self.ui.arithmetic,self.ui.geometric))

        self.ui.duplicate.clicked.connect(lambda: self.Duplicator())

        #setting an icon on few buttons
        dirname = os.path.dirname(__file__)

        self.ui.reloadReads.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'Refresh.png'))))
        self.ui.reloadReads.setText("reads")
        self.ui.reloadReads.setStyleSheet("Text-align:left")



        self.ui.setAnimated.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname,'key.png'))))
        self.ui.clearAnimated.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'nokey.png'))))
        self.ui.right.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'right.png'))))
        self.ui.up.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'up.png'))))
        self.ui.down.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'down.png'))))
        self.ui.left.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'left.png'))))

        self.ui.comment.clicked.connect(lambda: self.commentLead())

        self.ui.pBar.setMinimum(0)
        self.ui.pBar.setMaximum(100)
        self.ui.pBar.setToolTip("progress bar")


        #setting additional buttons

        self.ui.dummy1.setEnabled(True)
        self.ui.dummy1.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'flag.png'))))
        self.ui.dummy1.setText("start")
        self.ui.dummy1.clicked.connect(lambda: self.sScript())
        self.ui.dummy1.setStyleSheet("Text-align:left")
        self.ui.dummy1.setToolTip("script start template BackDrops")

        self.ui.dummy1_2.setEnabled(True)
        self.ui.dummy1_2.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'rv.png'))))
        self.ui.dummy1_2.setText("add")
        self.ui.dummy1_2.clicked.connect(lambda: self.RVtrixAdd())
        self.ui.dummy1_2.setStyleSheet("Text-align:left")
        self.ui.dummy1_2.setToolTip("add selected nodes to running rv session")



        self.ui.dummy1_4.setEnabled(True)
        self.ui.dummy1_4.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'cmpElem.png'))))
        self.ui.dummy1_4.setText("Elem")
        self.ui.dummy1_4.clicked.connect(lambda: self.compElemCreate())
        self.ui.dummy1_4.setToolTip("Create a comp element script from selected nodes")

        self.ui.dummy1_5.setEnabled(True)
        self.ui.dummy1_5.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'Time1.png'))))
        self.ui.dummy1_5.setText("share")
        self.ui.dummy1_5.clicked.connect(lambda: self.shareNodes())
        self.ui.dummy1_5.setToolTip("share Nodes Instantly")

        self.ui.dummy1_6.setEnabled(True)
        self.ui.dummy1_6.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'rv.png'))))
        self.ui.dummy1_6.setText("open")
        self.ui.dummy1_6.clicked.connect(lambda: self.RVtrix())
        self.ui.dummy1_6.setStyleSheet("Text-align:left")
        self.ui.dummy1_6.setToolTip("open selected nodes in RV player")

        self.ui.dummy1_10.setEnabled(True)
        self.ui.dummy1_10.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'Traktor.png'))))
        self.ui.dummy1_10.setText("farm")
        self.ui.dummy1_10.clicked.connect(lambda: self.tRend())
        self.ui.dummy1_10.setToolTip("render selected nodes on the render farm")

        # self.ui.dummy1_8.setEnabled(True)
        # self.ui.dummy1_8.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'rv.png'))))
        # self.ui.dummy1_8.setText("8")
        #self.ui.dummy1_10.setToolTip("render selected nodes on the render farm")

        
################################
        self.ui.dummy1_8.setEnabled(True)
        self.ui.dummy1_8.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'rv.png'))))
        self.ui.dummy1_8.pressed.connect(lambda: self.clearView())
        self.ui.dummy1_8.released.connect(lambda: self.unClearView())

##############################




        self.ui.dummy1_9.setEnabled(True)
        self.ui.dummy1_9.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'workflow.png'))))
        self.ui.dummy1_9.setText("lSet")
        self.ui.dummy1_9.clicked.connect(lambda: self.layerset())
        self.ui.dummy1_9.setStyleSheet("Text-align:left")
        self.ui.dummy1_9.setToolTip("Arnold(5) layer Set")


        self.ui.dummy1_7.setEnabled(True)
        self.ui.dummy1_7.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'eyes.png'))))
        self.ui.dummy1_7.setText("")
        self.ui.dummy1_7.clicked.connect(lambda: self.verSubmit())
        self.ui.dummy1_7.setToolTip("Submit selected Read node to review")

        self.ui.dummy1_11.setEnabled(True)
        self.ui.dummy1_11.setText("Load")
        self.ui.dummy1_11.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'cap.png'))))
        self.ui.dummy1_11.clicked.connect(lambda: self.createAssetLoader())
        self.ui.dummy1_11.setToolTip("Beta version of the Asset Loader by Ernest Dios/Adrian Pueyo")
        
        self.ui.dummy1_12.setEnabled(True)
        # self.ui.dummy1_12.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'nuke.png'))))
        self.ui.dummy1_12.setText("")
        self.ui.dummy1_12.clicked.connect(lambda: self.openInNautilus())
        self.ui.dummy1_12.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'Explorer.png'))))
        # self.ui.dummy1_12.setStyleSheet("Text-align:left")
        self.ui.dummy1_12.setToolTip("open location of selected Read node in Finder")

        self.ui.dummy1_13.setEnabled(True)
        self.ui.dummy1_13.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(dirname, 'balance.png'))))
        self.ui.dummy1_13.setText("")
        self.ui.dummy1_13.clicked.connect(lambda: self.med())



    # def killTMPs(self):
    #     import os
    #     a = nuke.selectedNodes()
    #     for n in a:
    #         file = n['file'].value().rpartition("/")[0]+"/"
    #         print file
    #         all = os.listdir(file)
    #         for one in all:
    #             if "tmp" in one:
    #                 os.remove(file+ one)
    def event(self, the_event):
        if the_event.type() == QtCore.QEvent.Type.Show:
            try:
                killPaneMargins(self)
            except:
                pass
        return super(MassivePanelPySide, self).event(the_event)
    def shareNodes(self):
        import tempShare
        tempShare.tempShare()

    def compElemCreate(self):
        from saveCompElements import saveCompElements 
        saveCompElements.showDialog()

    def openInNautilus(self):
        import Explorer
        Explorer.ExplorerJPEG()

    def verSubmit(self):
        import publisher
        publisher.publisher()

    def med(self):
        import subprocess
        subprocess.Popen(["/usr/bin/vlc","/corky/projects/Library/Tutorials/UnderUserStuff/AfterReview.mp4"])

    def sScript(self):
        import scriptStart
        scriptStart.scriptStart()

    def layerset(self):
        #import LayersetArnold as la
        #la.layersetArnold()
        #la.cryptoUpdate()
        import arnoldLayerSetTemplates;a=arnoldLayerSetTemplates.TemplateSelector();a.show()

    def tRend(self):
        import TrixterRender
        #TrixterRender()
        TrixterRender.trixterRender(0)

    def lRend(self):
        from menu import localRenderTRX
        localRenderTRX()

    def RVtrix(self):
        import rvPlay
        rvPlay.rvTrixter()

    def RVtrixAdd(self):
        import rvPlay
        rvPlay.rvPushTrixter()

    #trixter loader by ernest dios
    def createAssetLoaderOld(self):
        import ED_AssetLoader_Beta
        # declare the global
        global AssetLoaderPanel
        # create a static instance of your panel
        AssetLoaderPanel = ED_AssetLoader_Beta.ED_AssetLoader
        ED_AssetLoader_Beta.loadED_AssetLoader()
        def updateAssetLoader():
            AssetLoaderPanel.retrieveShotData()     
        nuke.addOnScriptSave(updateAssetLoader) #EVERY TIME WE SAVE WE UPDATE THE ASSET LOADER FOR EXEMPLE WHEN WE SET THE TRIXTER SHOT DATA


    def createAssetLoader(self):
        import ED_AssetLoader_BetaB
        ED_AssetLoader_BetaB.makeAssetLoader(autoGather=True)


    def clearView(self):   
        nuke.selectConnectedNodes()
        selected = nuke.selectedNodes()
        nuke.invertSelection()
        unselected = nuke.selectedNodes()

        for one in unselected:
            if one.Class() not in ["StickyNote",'BackdropNode']:
                one['xpos'].setValue(one['xpos'].value()+10000)   
            one.setSelected(False)
        for one in selected:
            one.setSelected(True)


    def unClearView(self):   
        nuke.selectConnectedNodes()
        selected = nuke.selectedNodes()
        nuke.invertSelection()
        unselected = nuke.selectedNodes()

        for one in unselected:
            if one.Class() not in ["StickyNote",'BackdropNode']:
                one['xpos'].setValue(one['xpos'].value()-10000)
            one.setSelected(False)
        for one in selected:
            one.setSelected(True)

    #comment backdrop
    def commentLead(self):
        import getpass 
        username = getpass. getuser()
        panel = nuke.Panel("comment")
        panel.addSingleLineInput("comment:","")
        p = panel.show()
        comment = panel.value('comment:')
        if p:
            bd = nukescripts.autoBackdrop()
            bd.knob("tile_color").setValue(4282384383)
            bd.knob('label').setValue(username+": "+comment)
    #duplicate selected node
    def Duplicator(self):
            panel = nuke.Panel("Duplicator")
            panel.addSingleLineInput("Copies:","10")
            panel.addSingleLineInput("Maximum nodes per row:","10")


            if panel.show():
                count = int(panel.value("Copies:"))
                c=count
                row = int(panel.value("Maximum nodes per row:"))
                node = nuke.selectedNode()
                nodes = [node]
                x = int(node['xpos'].value())
                basex = x
                y = int(node['ypos'].value())
                nuke.nodeCopy("%clipboard%")



                for i in range(count-1):
                    self.ui.pBar.setValue(i*100/c)
                    nuke.nodePaste("%clipboard%")
                    nodes.append(nuke.selectedNode())
                self.ui.pBar.setValue(0)
                Xoffset = 0
                Yoffset = 0
                count = 1
                c = len(nodes)
                for node in nodes:
                    self.ui.pBar.setValue(count*100/c)
                    node.setXYpos(x+Xoffset,y+Yoffset)
                    Xoffset = Xoffset + 100
                    rest = count%row
                    if rest == 0:
                        Yoffset = Yoffset+70
                        Xoffset = 0

                    count = count+1
                    node.setInput(0,None)
                    node.setSelected(True)
                self.ui.pBar.setValue(0)
    #toggle progression
    def incrProgressA(self,a,g):
        if a.isChecked():
            g.setChecked(False)
        else:
            g.setChecked(True) 
    def incrProgressG(self,a,g):
        if g.isChecked():
            a.setChecked(False)
        else:
            a.setChecked(True)        
    
    #set colors to nodes
    def setNodesColor(self,color):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            a = self.selectedNodesInContext()
            self.countSelectedNodes()
            i=1
            for n in a:
                    self.ui.pBar.setValue(i*100/len(a))
                    n['tile_color'].setValue(color)
                    i=i+1
            self.ui.pBar.setValue(0)
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback;
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    #collect memories and create dropdown menu
    def grabMemory(self,kind,memory):
        try:
            memo = nuke.toNode("root")['massiveMemory'].value()
            memory.clear()
            kind = kind.currentText()
            cells = memo.split('|')
            goodCells =["memory"]
            for one in cells:
                if kind in one:
                    goodCells.append(one)
            for one in goodCells:
                memory.addItem(one)
        except:
            pass
    
    # setting values from memory
    def setMemory(self, memory):
        #print memory.currentText()
        memoryList = memory.currentText()
        memoryList=memoryList.replace(" ","")
        memory = memoryList.split(",")
        self.ui.knob.setText(memory[0])
        self.ui.value.setText(memory[1])
        self.ui.increment.setText(memory[2])
        if memory[3] == "1":
            self.ui.red.setChecked(True)
        else:
            self.ui.red.setChecked(False)
        if memory[4] == "1":
            self.ui.green.setChecked(True)
        else:
            self.ui.green.setChecked(False)
        if memory[5] == "1":
            self.ui.blue.setChecked(True)
        else:
            self.ui.blue.setChecked(False)
        if memory[6] == "1":
            self.ui.alpha.setChecked(True)
        else:
            self.ui.alpha.setChecked(False)

    #creating memory knob on the root and storing values
    def massiveMemory(self,knob,value,increment,red,green,blue,alpha,kind): 
        b = nuke.toNode("root")#check if knob exist, if not will create it
        count = 0
        for i in range (b.getNumKnobs()):
            if b.knob(i).name() == "massiveMemory":
                count = 1 
            else:
                pass
        if count == 0:
            b.addKnob(nuke.String_Knob("massiveMemory","massiveMemory",))
        brain = b["massiveMemory"]
        #brain.setVisible(False)
        current = brain.getValue()
        if red.isChecked():
            red = "1"
        else:
            red = "0"
        if blue.isChecked():
            blue = "1"
        else:
            blue = "0"
        if green.isChecked():
            green = "1"
        else:
            green = "0"
        if alpha.isChecked():
            alpha = "1"
        else:
            alpha = "0"
        #update = knob.text()+","+value.text()+","+increment.text()+","+red+","+green+","+blue+","+alpha+","+kind.currentText()
        v = 20-len(value.text());vv = v*" "
        i = 20-len(increment.text());ii = i*" "
        aa = 16*" "
        k = 20-len(kind.currentText());kk = k*" "
        update = knob.text()+","+vv+value.text()+","+ii+increment.text()+","+aa+red+","+green+","+blue+","+alpha+","+kk+kind.currentText()
        new = current + "|" + update
        brain.setValue(new)
    
    # adding autocomplete to knob knob
    def gotFocusEvent(self,emittor):
        if emittor == self.ui.knob:
            listOfKnobs = []
            b = self.selectedNodesInContext()[0]
            for i in range (b.getNumKnobs()):
                knob =  b.knob (i).name()
                listOfKnobs.append(knob)
            completer = QCompleter(listOfKnobs, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.ui.knob.setCompleter(completer)
    
    #focusing on knobs
    def focusEvent(self,emittor):
        if emittor == self.ui.knob:
            self.ui.value.setFocus()
        elif emittor == self.ui.value:
            self.ui.increment.setFocus()
        elif emittor == self.ui.increment:
            self.ui.go.setFocus()
        elif emittor == self.ui.find:
            self.ui.replace.setFocus()
        elif emittor == self.ui.replace:
            self.ui.go.setFocus()

    # make nuke.selectedNodes work inside the group
    def selectedNodesInContext(self):
        # iterates through all widgets to get the currently visible DAG to get selected Nodes within a group
        currentDAG = ''

        if nuke.NUKE_VERSION_MAJOR < 11:
            allWidgets = QtGui.QApplication.instance().allWidgets()
        else:
            allWidgets = QtWidgets.QApplication.instance().allWidgets()
        
        for w in allWidgets:
            if 'DAG' in w.objectName() and w.isVisible():
                currentDAG = w.windowTitle()
        if currentDAG and currentDAG != 'Node Graph':
            group = nuke.toNode(currentDAG.replace(' Node Graph',''))
            with group:
                return nuke.selectedNodes()
        else:
            return nuke.selectedNodes()
    
    # make nuke.allNodes work inside the group
    def allNodesInContext(self):
        # iterates through all widgets to get the currently visible DAG to get selected Nodes within a group
        currentDAG = ''
        if nuke.NUKE_VERSION_MAJOR < 11:
            allWidgets = QtGui.QApplication.instance().allWidgets()
        else:
            allWidgets = QtWidgets.QApplication.instance().allWidgets()
        for w in allWidgets:
            if 'DAG' in w.objectName() and w.isVisible():
                currentDAG = w.windowTitle()
        if currentDAG and currentDAG != 'Node Graph':
            group = nuke.toNode(currentDAG.replace(' Node Graph',''))
            with group:
                return nuke.allNodes()
        else:
            return nuke.allNodes()

    #positon nodes in checkerboard pattern
    def checkerboardNodesAll(self):
        '''Original code written by Howard Jones, implemented in Massive panel by Alexey Kuchinsky
        '''
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            count=0
            moveBy=75
            
            for i in self.selectedNodesInContext():
                self.ui.pBar.setValue((count+1)*100/len(self.selectedNodesInContext()))
                m=count%3
                i.autoplace()
                i.setXYpos(i.xpos(), i.ypos()+(m*moveBy))
                count+=1
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
        self.ui.pBar.setValue(0)
    # allign nodes horizontally or vertically 
    def alignNodes(self, nodes, direction = 'x' ):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            '''
            Align nodes either horizontally or vertically.
            Original code written by Frank Rueter, implemented in Massive panel by Alexey Kuchinsky
            '''
            if len( nodes ) < 2:
                undo.end()#;print "undo end"
                return
            if direction.lower() not in ('x', 'y'):
                raise ValueError, 'direction argument must be x or y'

            positions = [ float( n[ direction.lower()+'pos' ].value() ) for n in nodes]
            avrg = sum( positions ) / len( positions )
            count = 1
            for n in nodes:
                self.ui.pBar.setValue((count+1)*100/len(nodes))
                if direction == 'x':
                    for n in nodes:
                        n.setXpos( int(avrg) )
                else:
                    for n in nodes:
                        n.setYpos( int(avrg) )
                count = count +1
            self.countSelectedNodes()
            undo.end()#;print "undo end"
            return avrg
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
        self.ui.pBar.setValue(0)
    # set knob animated. set keyframe
    def setAnimatedNodes(self, knob):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            knobVal = knob.text()
            nodesA = self.selectedNodesInContext()
            for nodeA in nodesA:
                nodeKnobVal = nodeA[knobVal].value()
                nodeA[knobVal].setAnimated()
                nodeA[knobVal].setValue(nodeKnobVal)          
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    # clear animation from selected knob
    def clearAnimatedNodes(self,knob):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            string = knob.text()
            nodesA = self.selectedNodesInContext()
            for nodeA in nodesA:
                nodeA[string].clearAnimated()
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    # scale nodes in the nodegraph 
    def scaleNodes(self,xScale, yScale=None ):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin scale"
        try:
            def getSideNodes( bd ):
                '''
                Original code written by Frank Rueter, implemented in Massive panel by Alexey Kuchinsky
                return a given backdrop node's "side nodes" (left, right, top andbottom most nodes) as a dictionary including the nodes and the respective DAG coordinates'''
                origSel = self.selectedNodesInContext()
                [ n.setSelected( False ) for n in origSel ]
                
                bd.selectNodes()
                bdNodes = self.selectedNodesInContext()
                [ n.setSelected( False ) for n in bdNodes ]  #DESELECT BACKDROP NODES
                [ n.setSelected( True ) for n in origSel ]  #RESTORE ORIGINAL SELECTION  
                if not bdNodes:
                    return []
                
                leftNode = rightNode = bottomNode = topNode= bdNodes[0] # START WITH RANDOM NODE
                for n in bdNodes:
                    if n.xpos() < leftNode.xpos():
                        leftNode = n
                    if n.xpos() > rightNode.xpos():
                        rightNode = n
                    if n.ypos() < topNode.ypos():
                        topNode = n
                    if n.ypos() > bottomNode.ypos():
                        bottomNode = n

                return dict( left=[leftNode, nuke.math.Vector2( leftNode.xpos(), leftNode.ypos()) ], right=[rightNode, nuke.math.Vector2( rightNode.xpos(), rightNode.ypos()) ], top=[topNode, nuke.math.Vector2( topNode.xpos(), topNode.ypos()) ], bottom=[bottomNode, nuke.math.Vector2( bottomNode.xpos(), bottomNode.ypos()) ])
                self.ui.pBar.setValue(0)
           # MAKE THINGS BACKWARDS COMPATIBLE
            yScale = yScale or xScale

           # COLLECT SIDE NODES AND COORDINATES FOR BACKDROPS
            backdrops = {}
            for bd in self.allNodesInContext():
                if 'BackdropNode' in bd.Class() :
                    backdrops[bd] = getSideNodes( bd )

            # MOVE NODES FROM CENTRE OUTWARD
            nodes = [ n for n in self.selectedNodesInContext() if n.Class() != 'BackdropNode' ]
            amount = len( nodes )
            if amount == 0:    
                undo.end()#;print "undo end"
                return

            allX = 0
            allY = 0
            for n in nodes:
                allX += n.xpos()
                allY += n.ypos()

            centreX = allX / amount
            centreY = allY / amount
            count = 1
            for n in nodes:
                n.setXpos( int( centreX + ( n.xpos() - centreX ) * xScale ) )
                n.setYpos( int( centreY + ( n.ypos() - centreY ) * yScale ) )
                self.ui.pBar.setValue(count*100/len(nodes))
                count+=1
            #ADJUST BACKDROP NODES
            # for bd,bdSides in backdrops.iteritems():
            #     leftDelta = bdSides['left'][0].xpos() - bdSides['left'][1].x
            #     topDelta = bdSides['top'][0].ypos() - bdSides['top'][1].y
            #     rightDelta = bdSides['right'][0].xpos() - bdSides['right'][1].x
            #     bottomDelta = bdSides['bottom'][0].ypos() - bdSides['bottom'][1].y


            #     bd.setXpos( int( bd.xpos() + leftDelta ) )
            #     bd.setYpos( int( bd.ypos() + topDelta ) )

            #     bd['bdwidth'].setValue( int( bd['bdwidth'].value() - leftDelta + rightDelta ) )
            #     bd['bdheight'].setValue( int( bd['bdheight'].value() - topDelta + bottomDelta ) )
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:

            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    # disable or enable icons on nodes    
    def iconCheck(self,lab,node):
        if self.ui.icons.isChecked():
            node['icon'].setValue("")
        else:
            node['icon'].setValue(lab)
            print "set label"

    #implementation of Go section
    def goGo(self,go,knob,value,inc,red,green,blue,alpha,kind,arithmetic,geometric): 
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            def knobCheck(dude):
                n= self.selectedNodesInContext()[0]
                knob = n[dude]
                if knob.Class() == "Int_Knob" or knob.Class() == "ColorChip_Knob":
                    return False
                else:
                    return True
            valKnob = knob.text()
            valValue = value.text()
            valIncrement = inc.text()
            if not inc.text():
                valIncrement = 0
            valVariable = 0
            valKind = kind.currentText()
            valRed = red.isChecked()
            valGreen = green.isChecked()
            valBlue = blue.isChecked()
            valAlpha = alpha.isChecked()
            valArray = [valRed,valGreen,valBlue,valAlpha]
            knobIsFloat = knobCheck(valKnob)
            fullHouse = 0
            if False not in valArray:
                fullHouse = 1
            def updatePanel(knob):# update properties panel
                node[knob].setFlag( nuke.INVISIBLE ) 
                node[knob].clearFlag( nuke.INVISIBLE ) 
            selNodes = list(reversed(self.selectedNodesInContext()))
            count = 1
            if valKind  == "number":            #setting number#######################################

                if arithmetic.isChecked():
                    incrementBase = 0
                else:
                    incrementBase = 0       
                ##print 'setting number'
                if knobIsFloat:                                                 #checking if knob is expecting a float or init     
                    incrementBase = float(incrementBase)
                    valIncrement = float(valIncrement)                         
                else:
                    incrementBase = int(incrementBase)
                    valIncrement = int(valIncrement)             
                for node in selNodes:
                    self.ui.pBar.setValue((count)*100/len(selNodes))
                    count+=1
                    if fullHouse == 0:
                        node[valKnob].setSingleValue(False)
                    for i, j in enumerate(valArray):                                                        
                        if j == True:
                            if "to" in valValue and 'val' not in valValue:#######setting random values!!!!!!
                                low = float(eval(valValue.rpartition("to")[0]))*1000
                                high = float(eval(valValue.rpartition("to")[2]))*1000                                     
                                randomValue = float(random.randint(low,high))/1000
                                node[valKnob].setValue(randomValue+incrementBase,i)
                            elif 'val' in valValue and 'to' not in valValue:######setting values relatively to the current value!!!!
                                oldVal = node[valKnob].value(i)
                                newVal = eval(valValue.replace("val",str(oldVal)))
                                node[valKnob].setValue(newVal+incrementBase,i)
                            elif 'val' in valValue and 'to' in valValue:######setting random values relatively to the current value!!!
                                low = float(valValue.rpartition("to")[0].rpartition("(")[2])*1000
                                high = float(valValue.rpartition("to")[2].rpartition(")")[0])*1000
                                oldVal = node[valKnob].value(i)
                                newVal =oldVal+float(random.randint(low,high))/1000
                                node[valKnob].setValue(newVal+incrementBase,i)
                            else:######setting value
                                if knobIsFloat:
                                    try:
                                        node[valKnob].setValue(float(valValue)+incrementBase,i)
                                    except:
                                        node[valKnob].setValue(float(valValue))
                                else:
                                    try:
                                        node[valKnob].setValue(int(valValue)+incrementBase,i)
                                    except:
                                        node[valKnob].setValue(int(valValue))


                    if fullHouse == 1:
                        node[valKnob].setSingleValue(True)
                    updatePanel(valKnob)
                    if arithmetic.isChecked():
                        incrementBase = valIncrement+incrementBase
                    else:
                        if incrementBase == 0:
                            incrementBase = 1
                        incrementBase = valIncrement*incrementBase
                self.ui.pBar.setValue(0)
            elif valKind == 'text':             #setting text########################################
                ##print 'setting expression'
                loop = 0
                if valIncrement != 0:
                    if float(valIncrement) % 1 == 0:
                        valIncrement = int(valIncrement)
                    else:
                        valIncrement = float(valIncrement)
                    loopValue = valValue.replace("var","0")
                    baseValIncrement = valIncrement


                for node in selNodes:
                    self.ui.pBar.setValue((count)*100/len(selNodes))
                    if valIncrement !=0:
                        if loop >0:
                            loopValue = valValue.replace("var",str(valIncrement))

                            if arithmetic.isChecked() :
                                if isinstance(baseValIncrement, int):
                                    valIncrement = str(int(valIncrement) + baseValIncrement)
                                else:
                                    valIncrement = str(float(valIncrement) + baseValIncrement)
                            else:
                                if isinstance(baseValIncrement, int):
                                    valIncrement = str(int(valIncrement) * baseValIncrement)
                                else:
                                    valIncrement = str(float(valIncrement) * baseValIncrement)
                    else:
                        loopValue = valValue
                        print valValue
                    if True not in valArray or False not in valArray:                   #setting one value to all array members                                                                                                       
                                if valKnob == "name":
                                    node.setName(str(loopValue))
                                else:
                                    print loopValue
                                    node[valKnob].setValue(str(loopValue))
                    else:                                                               # setting separated values to members
                        ##print "array found"                
                        for i, j in enumerate(valArray):                                                        
                            if j == True:
                                if valKnob == "name":
                                    node.setName(str(loopValue),i)
                                else:
                                    node[valKnob].setValue(str(loopValue),i)

                    loop = loop+1
                    count+=1
                self.ui.pBar.setValue(0)
            elif valKind == 'expression':       #setting expression#######################################
                ##print 'setting expression'
                loop = 0
                baseValIncrement = valIncrement
                loopValue = valValue.replace("var","0")
                for node in selNodes:
                    self.ui.pBar.setValue((count)*100/len(selNodes))
                    if loop >0:
                        loopValue = valValue.replace("var",str(valIncrement))
                        if arithmetic.isChecked():
                            valIncrement = str(float(valIncrement) + float(baseValIncrement))
                        else:
                            valIncrement = str(float(valIncrement) * float(baseValIncrement))                            
                    if True not in valArray or False not in valArray:                   #setting one value to all array members                                                                                                       
                                node[valKnob].setExpression(loopValue)
                    else:                                                               # setting separated values to members
                        ##print "array found"                
                        for i, j in enumerate(valArray):                                                        
                            if j == True:
                                    node[valKnob].setExpression(loopValue,i)
                    loop = loop+1
                    count+=1
                    ##print valIncrement
            self.ui.pBar.setValue(0)
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    # implementation of take buttons
    def setTake(self,button,res,dis_en,low,high,sel,icon):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        
        try:
            self.countSelectedNodes()
            #gasering information
            label = button.text()
            name = button.objectName()
            lowVal = low.text()
            highVal = high.text()
            knobVal = "fuckOff"
            sameName = 0

            # guessing what is the knob to be affected
            a = self.selectedNodesInContext()
            b = self.selectedNodesInContext()[0].knobs()
            if "samples" in b: 
                knobToAffect = 'samples'
            elif "motionblur" in b:
                knobToAffect = "motionblur"
            elif "which" in b:
                knobToAffect = "which"
            else:
                knobToAffect = "disable"

            # guessing default value  
            if lowVal == "":
                if "samples" in b: 
                    lowVal = 1;highVal = 16
                elif "motionblur" in b or "which" in b:
                    lowVal = 0;highVal = 1
                else:
                    lowVal = 1;highVal = 0
      
            #collecting information needed to set a label
            if "Take" in label or "++"+label+"++"  in a[0]['label'].value():#if button is fresh or belongs to same take
                button.setStyleSheet('QPushButton {color: white;}')
                res.setStyleSheet('QPushButton {color: white;}')
                dis_en.setStyleSheet('QPushButton {color: white;}')
                low.setStyleSheet('QPushButton {color: rgb(50,50,50);}')
                high.setStyleSheet('QPushButton {color: rgb(50,50,50);}')
                sel.setStyleSheet('QPushButton {color: white;}')

                if "++"+label+"++"  in a[0]['label'].value():
                    panel = nuke.ask("looks like yo want to change take's properties, is this the case?")
                    if panel:
                        panel = nuke.Panel("setLabel")
                        panel.addSingleLineInput("take name",label)
                        panel.addSingleLineInput("knob to affect",knobToAffect)
                        panel.addSingleLineInput("low",lowVal)
                        panel.addSingleLineInput("high",highVal)

                        panel.show()

                        takeName = panel.value("take name")
                        knobToAffect = panel.value("knob to affect")
                        lowVal = panel.value("low")
                        highVal = panel.value("high")


                        sameName = 1
                #if take is already assigned
                else:
                    
                    panel = nuke.Panel("setLabel")
                    panel.addSingleLineInput("take name","")
                    panel.addSingleLineInput("knob to affect",knobToAffect)
                    panel.addSingleLineInput("low",lowVal)
                    panel.addSingleLineInput("high",highVal)

                    panel.show()

                    takeName = panel.value("take name")
                    knobToAffect = panel.value("knob to affect")
                    lowVal = panel.value("low")
                    highVal = panel.value("high")


                    if not takeName:#if pressing okay
                        takeName = label
            else:#if button is not fresh, assign some nodes to some take
                panel = nuke.ask("you going to assign selected nodes to "+label+"\nare you sure about that?")
                if panel:#if pressing okay
                    takeName = label
                    if dis_en.text() == "E":
                        knobVal = highVal
                    if dis_en.text() == "D":
                        knobVal = lowVal
                else:#if canceling
                    pass

            

            ##setting take label and additional knobs to selected nodes
            if "++" in a[0]['label'].value():# if node belongs to other take
                if sameName == 1:
                    pass
                else:
                    panel = nuke.ask("looks like one or more selected nodes belongs to other take\nare you sure you want to add them to "+takeName+"?")
                if panel or sameName == 1:#if pressing okay
                    for n in a:
                        try:
                            n.removeKnob(n.knobs()["l_h"])
                            n.removeKnob(n.knobs()["takeCode"])
                            n.removeKnob(n.knobs()["takeName"])
                            n.removeKnob(n.knobs()["affectedKnob"])
                        except:
                            pass
                        n['label'].setValue("++"+takeName+"++")

                        #adding additional knobs
                        t = nuke.Text_Knob("takeCode","take code",name)
                        nn = nuke.Text_Knob("takeName","take name",takeName)
                        ak = nuke.Text_Knob("affectedKnob","affected knob",knobToAffect)
                        g = nuke.XY_Knob("l_h","low/high values")

                        kn = [t,nn,ak,g]
                        for knobb in kn:
                            n.addKnob(knobb)

                        n['l_h'].setValue([lowVal,highVal])


            else:  # if node does not belong to other take
                for n in a:
                    if n['label'].value() == "":#if label of selected node is empty
                        n['label'].setValue(n['label'].value()+"++"+takeName+"++")

                    else:# if label is not empty
                        n['label'].setValue(n['label'].value()+"\n"+"++"+takeName+"++")

                    #adding additional knobs
                    t = nuke.Text_Knob("takeCode","take code",name)
                    nn = nuke.Text_Knob("takeName","take name",takeName)
                    ak = nuke.Text_Knob("affectedKnob","affected knob",knobToAffect)
                    g = nuke.XY_Knob("l_h","low/high values")

                    kn = [t,nn,ak,g]
                    for knobb in kn:
                        n.addKnob(knobb)

                    n['l_h'].setValue([lowVal,highVal])


                    if knobVal != "fuckOff":
                        n[knobToAffect].setValue(knobVal)


            #setting values to the Massive panel
            if takeName:# setting label to the take button
                button.setText(takeName)
                #button.setToolTip(knobToAffect)

            #hiding low/high knobs if disable knob will be operated

            # if knobToAffect == "disable":
            #     low.hide()
            #     high.hide()

            #setting low and high values
            low.setText(str(lowVal))
            high.setText(str(highVal))
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    #implementation of select buttons
    def selectTake(self,button,res,dis_en,low,high,sel): #
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"

        try:
            label = button.text()
            a = self.allNodesInContext()
            for one in a:
                l = one['label'].value()
                if "++"+label+"++" in l:
                    one.setSelected(True)
                else:
                    one.setSelected(False)
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    #implementation of disable buttons
    def disableTake(self,button,res,dis_en,low,high,sel,icon): 
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            take_text = button.text()
            dis_en_text = dis_en.text()
            lowVal = low.text()
            highVal = high.text()
            a = self.allNodesInContext()
            nodesToDisable = []
            for one in a:#find all needed nodes
                if "++"+take_text+"++" in one['label'].value():
                    nodesToDisable.append(one)
            #toggle enable and disable
            if dis_en_text == "D":  
                for node in nodesToDisable:
                    knobToAffect = node['affectedKnob'].value()
                    node[knobToAffect].setValue(float(highVal))
                    node['note_font_color'].setValue(3342591) 
                    node['l_h'].setValue([lowVal,highVal])
                    #node['icon'].setValue("enabled.png")
                    self.iconCheck("enabled.png",node)
                    dis_en.setText("E")
                    dis_en.setStyleSheet('QPushButton {background-color: rgb(60,100,60);}')
            if dis_en_text == "E" or dis_en_text == "T":
                for node in nodesToDisable:
                    knobToAffect = node['affectedKnob'].value() 
                    node[knobToAffect].setValue(float(lowVal))
                    node['note_font_color'].setValue(855638271)
                    node['l_h'].setValue([lowVal,highVal])
                    #node['icon'].setValue("disabled.png") 
                    self.iconCheck("disabled.png",node)

                    dis_en.setText("D")
                    dis_en.setStyleSheet('QPushButton {background-color: rgb(128,50,50);}')
            for one in nodesToDisable:
                one.setSelected(True)
            self.countSelectedNodes()
            for one in nodesToDisable:
                one.setSelected(False)
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage) 
    
    #implementation of reset take
    def resetTake(self,button,res,dis_en,low,high,sel): 
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:

            def grayOut(): #grayout certain take 
                button.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                res.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                dis_en.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                low.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                high.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                sel.setStyleSheet('QPushButton {color: rgb(62,62,62);}')
            label = button.text()
            selected = 0
            try:
                a = self.selectedNodesInContext()
                for one in a:
                    l = one['label'].value()
                    if "++"+label+"++" in l:
                        selected = 1
            except:
                pass

            if selected == 0:#reset take
                if nuke.ask('This will reset current Take, are you sure you up to it?'):
                    name = button.objectName().replace("take","")
                    button.setText("Take "+name)
                    dis_en.setText("D")
                    dis_en.setStyleSheet('QPushButton {color: "";}')
                    low.setPlaceholderText("low")
                    low.setText("")
                    low.show()
                    high.setPlaceholderText("high")
                    high.setText("")
                    high.show()
                    grayOut()

                    a = self.allNodesInContext()
                    for one in a:
                        l = one['label'].value()
                        if "++"+label+"++" in l:
                            #one['note_font_color'].setValue(0)
                            ##print "++"+label+"++"
                            one['label'].setValue(l.replace("++"+label+"++",""))
                            one['icon'].setValue("")
                            d_knobs = ["l_h","takeCode","affectedKnob","takeName"]
                            for knob in d_knobs:
                                one.removeKnob(one.knob(knob))

            else:#exclude selected node from a take
                        if nuke.ask('This will exclude selected nodes from Take, are you sure you up to it?'):
                            for one in a:
                                one['label'].setValue(l.replace("++"+label+"++",""))
                                #one['note_font_color'].setValue(0)
                                one['icon'].setValue("")
                                d_knobs = ["l_h","takeCode","affectedKnob","takeName"]
                                for knob in d_knobs:
                                    one.removeKnob(one.knob(knob))
            self.countSelectedNodes()
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    #refreshing the panel to get all the data back to the panel!!!
    def refreshTakes(self):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
                              
            takes1 = [self.ui.take1,self.ui.resetTake1,self.ui.disableTake1,self.ui.take1Low,self.ui.take1High,self.ui.selectTake1,self.ui.rotosMB,self.ui.icons]
            takes2 = [self.ui.take2,self.ui.resetTake2,self.ui.disableTake2,self.ui.take2Low,self.ui.take2High,self.ui.selectTake2,self.ui.rotosMB,self.ui.icons]
            takes3 = [self.ui.take3,self.ui.resetTake3,self.ui.disableTake3,self.ui.take3Low,self.ui.take3High,self.ui.selectTake3,self.ui.rotosMB,self.ui.icons]
            takes4 = [self.ui.take4,self.ui.resetTake4,self.ui.disableTake4,self.ui.take4Low,self.ui.take4High,self.ui.selectTake4,self.ui.rotosMB,self.ui.icons]
            takes5 = [self.ui.take5,self.ui.resetTake5,self.ui.disableTake5,self.ui.take5Low,self.ui.take5High,self.ui.selectTake5,self.ui.rotosMB,self.ui.icons]
            takes6 = [self.ui.take6,self.ui.resetTake6,self.ui.disableTake6,self.ui.take6Low,self.ui.take6High,self.ui.selectTake6,self.ui.rotosMB,self.ui.icons]
            takes7 = [self.ui.take7,self.ui.resetTake7,self.ui.disableTake7,self.ui.take7Low,self.ui.take7High,self.ui.selectTake7,self.ui.rotosMB,self.ui.icons]
            takes8 = [self.ui.take8,self.ui.resetTake8,self.ui.disableTake8,self.ui.take8Low,self.ui.take8High,self.ui.selectTake8,self.ui.rotosMB,self.ui.icons]
            takes9 = [self.ui.take9,self.ui.resetTake9,self.ui.disableTake9,self.ui.take9Low,self.ui.take9High,self.ui.selectTake9,self.ui.rotosMB,self.ui.icons]
            takes10 = [self.ui.take10,self.ui.resetTake10,self.ui.disableTake10,self.ui.take10Low,self.ui.take10High,self.ui.selectTake10,self.ui.rotosMB,self.ui.icons]
            takes11 = [self.ui.take11,self.ui.resetTake11,self.ui.disableTake11,self.ui.take11Low,self.ui.take11High,self.ui.selectTake11,self.ui.rotosMB,self.ui.icons]
            allTakes = [takes1,takes2,takes3,takes4,takes5,takes6,takes7,takes8,takes9,takes10,takes11]

            a = self.allNodesInContext()
            labels = []
            for one in a:                           #collecting all nodes labels
                labels.append(one['label'].value())

            for line in allTakes:                   #going through every take and checking it's status
                takeName = line[0].text()
                found = 0
                for one in a:#if take is found in the script data is collected
                    if "++" in one['label'].value():
                        takeCode = one['takeCode'].value()
                        if line[0].objectName() ==takeCode:
                            takeName = one['takeName'].value()
                            affectedKnob = one['affectedKnob'].value()
                            low = one['l_h'].value()[0]
                            high = one['l_h'].value()[1]
                            line[0].setText(takeName)
                            if one[affectedKnob].value() == high:    
                                line[2].setText("E")
                                line[2].setStyleSheet('QPushButton {background-color: rgb(60,100,60);}')
                            elif one[affectedKnob].value() == low:
                                line[2].setText("D")
                                line[2].setStyleSheet('QPushButton {background-color: rgb(128,50,50);}')
                            line[3].setText(str(low))
                            line[4].setText(str(high))
                            line[0].setStyleSheet('QPushButton {color: white;}')
                            line[1].setStyleSheet('QPushButton {color: white;}')
                            line[3].setStyleSheet('QPushButton {color: rgb(50,50,50);}')
                            line[4].setStyleSheet('QPushButton {color: rgb(50,50,50);}')
                            line[5].setStyleSheet('QPushButton {color: white;}')


                for one in labels:
                    if takeName in one:
                        found = 1
                if found ==0:#if take is not found in the script the take is resetted
                    name = line[0].objectName().replace("take","")
                    line[0].setText("Take "+name)
                    line[0].setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                    line[1].setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                    line[2].setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                    line[2].setText("D")
                    line[2].setStyleSheet('QPushButton {color: "";}')
                    line[3].setPlaceholderText("low")
                    line[3].setText("")
                    line[3].show()
                    line[3].setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                    line[4].setPlaceholderText("high")
                    line[4].setText("")
                    line[4].show()
                    line[4].setStyleSheet('QPushButton {color: rgb(62,62,62);}')
                    line[5].setStyleSheet('QPushButton {color: rgb(62,62,62);}')

            for one in a:
                    if 'Roto' in one.Class():
                        rotoExample = one
            try:
                if rotoExample['motionblur_mode'].value() == "shape":
                    takes1[6].setText("Rotos MB On")
                    takes1[6].setStyleSheet('QPushButton {background-color: rgb(60,100,60);}')
                else:
                    takes1[6].setText("Rotos MB Off")
                    takes1[6].setStyleSheet('QPushButton {background-color: rgb(128,50,50);}')  
            except:
                pass

            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    #toggle motionblur in roto and paint nodes
    def rotosMBtoggle(self,rotoButton,icon):        
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            rotoButton_text = rotoButton.text()
            a = self.allNodesInContext()
            nodesToDisable = []
            for one in a:                                                           #find all Roto and Rotoshape nodes
                if "Roto" in one.Class():
                    nodesToDisable.append(one)
                                                                                            
            if rotoButton_text == "Rotos MB Off":                                   #toggle enable and disable motion blur 
                for node in nodesToDisable:
                    node['motionblur_mode'].setValue('shape')
                    node['global_motionblur'].setValue(1)
                    node['icon'].setValue("")
                rotoButton.setText("Rotos MB On")
                rotoButton.setStyleSheet('QPushButton {background-color: rgb(60,100,60);}')
            if rotoButton_text == "Rotos MB On" or rotoButton_text == "Rotos MB":
                for node in nodesToDisable:
                    node['motionblur_mode'].setValue('global')
                    node['global_motionblur'].setValue(0)
                    #node['icon'].setValue("disabled.png")
                    self.iconCheck("disabled.png",node)
                rotoButton.setText("Rotos MB Off")
                rotoButton.setStyleSheet('QPushButton {background-color: rgb(128,50,50);}')


            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    # search and replace
    def searchAndReplace(self,find,replace,knob):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            self.countSelectedNodes()
            knob = knob.text()
            if knob == "":
                knob = "file"
            findSTR = find.text()
            replaceSTR = replace.text()
            replNodes = self.selectedNodesInContext()
            if findSTR =="":
                for boy in replNodes:
                    index = 0
                    fKnob = boy['file']
                    fileOld = fKnob.value()
                    lower = fileOld.find("_v")+2
                    higher = fileOld.find("_v")+5
                    oldVersion = fileOld[lower:higher]
                    fileNew = fKnob.setValue(fileOld.replace(oldVersion,str("%03d" % int(replaceSTR)) ))
            else:
                for boy in replNodes:
                    index = 0
                    if boy[knob].hasExpression(index):
                        newExpression = boy[knob].animation(index).expression().replace(findSTR,replaceSTR)
                        boy[knob].setExpression(newExpression, index)
                    elif isinstance(boy[knob].value(), float):
                         ##print "float"
                         newVal=eval(str(boy[knob].value()).replace(findSTR,replaceSTR))
                         boy[knob].setValue(newVal)
                    elif isinstance(boy[knob].value(), basestring):
                        ##print "string"
                        newVal = boy[knob].value().replace(findSTR,replaceSTR)
                        boy[knob].setValue(newVal)

            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
    
    # disable icons on nodes in the nodegraph
    def killIcons(self,icon):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            if self.ui.icons.isChecked():
                a = self.allNodesInContext()
                for node in a:
                    node['icon'].setValue("")
                    self.ui.icons.setText("Icons\noff")
            else:
                self.ui.icons.setText("Icons\non")
                pass
                print "fdfd"
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            print t
            nuke.message(t+"\n\n " + self.ui.errorMessage)

    # randomly connect nodes
    def randomConnectNodes(self):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            self.countSelectedNodes()
            try:
                memo = nuke.toNode("root")['randomMemo'].value()
            except:
                nuke.toNode("root").addKnob(nuke.String_Knob("randomMemo","randomMemo","your Basic Name,,,0"))
            name =  nuke.toNode("root")['randomMemo'].value().split(",")[0]
            low =  nuke.toNode("root")['randomMemo'].value().split(",")[1]
            high =  nuke.toNode("root")['randomMemo'].value().split(",")[2]
            inputNr =  nuke.toNode("root")['randomMemo'].value().split(",")[3]

            panel = nuke.Panel("select sourses")
            panel.addSingleLineInput("sourse basic name",name)
            panel.addSingleLineInput("sourse low",low)
            panel.addSingleLineInput("sourse high",high)
            panel.addSingleLineInput("input",inputNr)
            panel.show()
            name = panel.value("sourse basic name")
            low = panel.value("sourse low")
            high = panel.value("sourse high")
            inputNr = panel.value("input")

            nuke.toNode("root")['randomMemo'].setValue(name+","+low+","+high+","+inputNr)

            s = self.selectedNodesInContext()
            i =1
            for node in s:
                self.ui.pBar.setValue(i*100/len(s))
                dude = nuke.toNode(name+str(random.randint(int(low),int(high))))
                node.setInput(int(inputNr),dude)
                i = i+1
            undo.end()#;print "undo end"
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
        self.ui.pBar.setValue(0)
    # snap to vertices
    def snap3Dgeo(self):
        undo = nuke.Undo()
        undo.begin()#;print "undo begin"
        try:
            self.countSelectedNodes()
            numb = 0
            points = nukescripts.snap3d.selectedPoints()
            for p in points:
                numb = numb+1
            if self.selectedNodesInContext():
                nodes = self.selectedNodesInContext()
                count = 0
                try:
                    for point in nukescripts.snap3d.selectedPoints():
                        print point
                        self.ui.pBar.setValue((count+1)*100/numb)
                        nodes[count]['translate'].setValue(point)
                        count = count + 1
                except:
                    pass

            else:
                panel = nuke.Panel("create node")
                panel.addEnumerationPulldown('node', 'Axis Card Sphere Cube Cylinder Light Camera')
                panel.show()
                name = panel.value("node")
                count = 0
                i = 75
                g=1
                for point in nukescripts.snap3d.selectedPoints():
                    self.ui.pBar.setValue(g*100/numb)
                    node = nuke.createNode(name)
                    node['translate'].setValue(point)
                    node.setInput(0,None)
                    if count <1:
                        x = int(node['xpos'].value())
                        y = int(node['ypos'].value())
                        count = 1
                    else:
                        node.setXYpos(x+i,y)
                        i = i+75
                    g = g+1
            undo.end()#;print "undo end"
            self.ui.pBar.setValue(0)
        except:
            undo.end()#;print "undo end"
            import traceback; 
            t = traceback.format_exc()
            nuke.message(t+"\n\n " + self.ui.errorMessage)
                    
    # reload all read nodes in script
    def readsReload(self):
        a = nuke.allNodes("Read")
        i = 1
        for one in a:
            self.ui.pBar.setValue(i*100/len(a))
            one['reload'].execute()
            i = i+1
        self.ui.pBar.setValue(0)
    # count selected nodes
    def countSelectedNodes(self):
        n = len(self.selectedNodesInContext())
        self.ui.countSelected.setText(str(n))




########################################################################################################################################
def main():
    app = self.ui.QtWidgets.QApplication(sys.argv)
         # A new instance of QApplication
    form = MassivePanelPySide()                 # We set the form to be our MassivePanelPySide (design)
    form.show()                                 # Show the form
    app.exec_()
    #print "hallo"                                # and execute the app


if __name__ == '__main__':                      # if we're running file directly and not importing it
    main()                                      # run the main function


## make this work in a .py file and in 'copy and paste' into the script editor
moduleName = __name__
if moduleName == '__main__':
  moduleName = ''
else:
  moduleName = moduleName + '.'
panels.registerWidgetAsPanel(moduleName + 'MassivePanelPySide', 'MassivePanelPySide','uk.co.thefoundry.MassivePanelPySide')



# python C:\Python27\Lib\site-packages\PySide\scripts\uic.py J:\PySideTutorial\01_Projects\Massive_v19.ui -o F:\Dropbox\users\current\Mdev\mdev.py -x

#refresh will not work with no ops - no disable knob