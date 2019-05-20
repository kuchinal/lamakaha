
import nuke
import os
import getpass
import subprocess
from functools import partial
username = getpass.getuser()
admins = ["kuchinal","pueyoad","dioser","warlimmo","dohnemi"]

# PySide import switch
try:
    from PySide import QtGui, QtCore, QtGui as QtWidgets
except ImportError:
    from PySide2 import QtWidgets, QtGui, QtCore



def layersetArnold():
    try:
        g = nuke.selectedNode()
        g.setSelected(False)
    except:
        pass


    nuke.nodePaste('/corky/projects/RnD_00001/exchange/underUserAlexey/Scripts/ArnoldTemplate_v08.nk')
    panel = nuke.Panel("LayerSetName")
    panel.addSingleLineInput("I would kindly ask you to Name your layerset:","name me")
    if panel.show():
        nameS = panel.value("I would kindly ask you to Name your layerset:")


    a = nuke.selectedNodes()
    for node in a:
        try:
            if "Passes" in node['label'].value():
                node.setInput(0,g)
                x = int(node['xpos'].value())
                y = int(node['ypos'].value())
                g.setXYpos(x-34,y-100)
        except:
            pass

        if "LayerSetName" in node['name'].value():
            node['label'].setValue(nameS+"          .")

        if node.knob("identifier") and node.knob("tags"): 
            if node.knob("identifier").value() == "anchor":
                tags = node.knob("tags")
                tags.setValue(nameS)

        if "Cryptomatte" in node.Class():
            cryptoUpdate(node)
            tags_knob = nuke.String_Knob('stamp_tags','Tags', nameS)
            node.addKnob(tags_knob)

    # for nod in s:
    #     nod.setSelected(True)


def cryptoUpdate(n = nuke.thisNode()):
    try: 
        import cryptomatte_utilities as cu
        cu.update_cryptomatte_gizmo(nuke.thisNode(), True)
    except Exception, err:
        import traceback
        nuke.message('''Unable to run Cryptomatte Gizmo update script. This script is necessary for the Cryptomatte system to work properly. 
        %s''' % traceback.format_exc())




# pointing to the folder with templates
jobEnv = os.environ["JOB"]
pathToTemplates = "/corky/projects/"+jobEnv+"/library/compositing/ArnoldTreeTemplates/"
if os.path.isdir(pathToTemplates) is False:
    print "gdfgdfgfdgfd"
    os.mkdir(pathToTemplates)
scriptsFull =  os.listdir(pathToTemplates)
scripts = []
for one in scriptsFull:

    one = one.replace(".nk","")

    scripts.append(one)


#scripts.remove("UnderUser")
scripts.insert(0,"UnderUser")
#scripts.remove("BasicTRX")
scripts.insert(1,"BasicTRX")

scripts.append("")
scripts.remove("")
scripts.insert(2,"")
scripts.append("")
scripts.append("Add selected nodes as Template")
scripts.append("Dive into Templates directory")


#scripts = 
class TemplateSelector(QtWidgets.QDialog):
    '''
    Panel presenting available arnold templates.
    '''
    def __init__(self):
        super(TemplateSelector, self).__init__()
        self.setWindowTitle("Arnold Layerset templates")
        self.initUI()
        #self.custom_anchors_lineEdit.setFocus()
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.Popup)

        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)



    def initUI(self):

        # Layouts
        self.master_layout = QtWidgets.QVBoxLayout()
        for number, layerset in enumerate(scripts):   
            ok_btn = QtWidgets.QPushButton(layerset)
            ok_btn.setStyleSheet("background-color: dark gray;font: bold;Text-align:center;font-size:50px")

            #ok_btn.clicked.connect(lambda: clickedFocusEvent(shotKnob))


            if ok_btn.text()=="Add selected nodes as Template":
                ok_btn.setStyleSheet("Text-align:center;font-size:20px")
                ok_btn.clicked.connect(partial(self.bntSavePressed,layerset+".nk"))
                if username in admins:
                    ok_btn.setVisible(True)
                else:
                    ok_btn.setVisible(False)

            elif ok_btn.text()=="Dive into Templates directory":
                ok_btn.setStyleSheet("Text-align:center;font-size:20px")
                ok_btn.clicked.connect(lambda: self.bntDive() )
                if username in admins:
                    ok_btn.setVisible(True)
                else:
                    ok_btn.setVisible(False)

            elif ok_btn.text()=="":
                ok_btn.setMaximumHeight(10)
                ok_btn.setStyleSheet("background-color: black")

            elif ok_btn.text()=="UnderUser":
                ok_btn.clicked.connect(lambda: self.bntUnderUserPressed() )

            elif ok_btn.text()=="BasicTRX":
                ok_btn.clicked.connect(lambda: self.bntBasicPressed() )

            else:
                ok_btn.clicked.connect(partial(self.bntPressed,layerset))


            self.master_layout.addWidget(ok_btn)
        self.setLayout(self.master_layout)


    def bntUnderUserPressed(self):
        layersetArnold();cryptoUpdate()
        self.close()

    def bntBasicPressed(self):
        nuke.nodePaste("/mnt/repository/source_code/engines/nuke/devel/etc/nuke/templates/CG/CG_Template_XL.nk")
        self.close()

    def bntPressed(self,a):
        nuke.nodePaste(pathToTemplates+a+".nk")
        self.close()

    def bntSavePressed(self,a):
        panel = nuke.Panel("Name me!!!")
        panel.addSingleLineInput("Name:","")
        if panel.show():
            a = panel.value("Name:")
        nuke.nodeCopy(pathToTemplates+a)
        self.close()

    def bntDive(self):
        subprocess.Popen(['nautilus','%s' % (pathToTemplates)])
        self.close()
    
    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate,QtCore.QEvent.FocusOut]:
            self.close()
            return True
        return False

