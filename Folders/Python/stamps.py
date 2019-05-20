"""
Stamps rebuilt by Adrian Pueyo
Full original concept and Postage Stamps created by Alexey Kuchinski and Ernest Dios.
"""
version= "v0.2"

# Constants
STAMP_DEFAULTS = { "note_font_size":20, "hide_input":0 }
ANCHOR_DEFAULTS = { "tile_color" : int('%02x%02x%02x%02x' % (255,255,255,1),16),
        "autolabel": 'nuke.thisNode().knob("title").value()',
        "knobChanged":'import stamps; stamps.anchorKnobChanged()'}
WIRED_DEFAULTS = { "tile_color" : int('%02x%02x%02x%02x' % (1,0,0,1),16),
        "autolabel": 'nuke.thisNode().knob("title").value()',
        "knobChanged":'import stamps; stamps.wiredKnobChanged()'}
DeepExceptionClasses = ["DeepToImage","DeepHoldout"] # Nodes with "Deep" in their class that don't classify as Deep.
NodeExceptionClasses = ["Viewer"] # Nodes that won't accept stamps
ParticleExceptionClasses = ["ParticleToImage"] # Nodes with "Particle" in class and an input called "particles" that don't classify as particles.

StampClasses = {"2D":"NoOp", "Deep":"DeepExpression"}
AnchorClassColors = {"Camera":int('%02x%02x%02x%02x' % (255,0,0,1),16),
                     "3D":int('%02x%02x%02x%02x' % (255,0,0,1),16),}
WiredClassColors = {"Camera":int('%02x%02x%02x%02x' % (255,0,0,1),16),
                     "3D":int('%02x%02x%02x%02x' % (255,0,0,1),16),}
STAMPS_HELP = "Redone by Adrian Pueyo.\nUpdated 29 Mar 2019\n\nFull original concept and \"Postage Stamps\" created by Alexey Kuchinski."
VERSION_TOOLTIP = "Stamps \nRedone by Adrian Pueyo.\nFull original concept and \"Postage Stamps\" created by Alexey Kuchinski."

if not globals().has_key('Stamps_LastCreated'):
    Stamps_LastCreated = None

import nuke
import nukescripts
import re
from functools import partial

# PySide import switch
try:
    from PySide import QtGui, QtCore, QtGui as QtWidgets
except ImportError:
    from PySide2 import QtWidgets, QtGui, QtCore

#################################
### FUNCTIONS INSIDE OF BUTTONS
#################################
def wiredShowAnchor():
    n = nuke.thisNode()
    if n.inputs():
        nuke.show(n.input(0))

def wiredZoomAnchor():
    n = nuke.thisNode()
    if n.inputs():
        ni = n.input(0)
        nuke.zoom(nuke.zoom(),[ni.xpos()+ni.screenWidth()/2,ni.ypos()+ni.screenHeight()/2])

def wiredZoomThis():
    n = nuke.thisNode()
    nuke.zoom(nuke.zoom(),[n.xpos(),n.ypos()])

def wiredStyle(n, style = 0):
    ''' Change the style of a wired stamp, based on some presets '''
    nf = n["note_font"].value().split(" Bold")[0].split(" bold")[0]
    if style == 0: # DEFAULT
        n["note_font_size"].setValue(20)
        n["note_font_color"].setValue(0)
        n["note_font"].setValue(nf)
    elif style == 1: # BROKEN
        n["note_font_size"].setValue(40)
        n["note_font_color"].setValue(4278190335)
        n["note_font"].setValue(nf+" Bold")

def wiredKnobChanged():
    k = nuke.thisKnob()
    kn = k.name()
    if kn in ["xpos","ypos"]:
        return
    n = nuke.thisNode()
    ni = n.inputs()
    if n.knob("toReconnect") and n.knob("toReconnect").value() and nuke.GUI and not ni:
        try:
            inp = n.knob("anchor").value()
            a = nuke.toNode(inp)
            if a.knob("title") and n.knob("title") and a["title"].value() == n["title"].value():
                nuke.thisNode().setInput(0,a)
            else:
                wiredStyle(n,1)
            n.knob("toReconnect").setValue(False)
        except:
            pass
    elif kn == "selected": #First time it's this knob, it will activate the first if, then, ignore.
        return
    elif kn == "inputChange" or not ni:
        if not ni or (ni and not isAnchor(n.input(0))):
            wiredStyle(n,1)
        elif n.input(0).knob("title") and n.knob("title") and n.input(0)["title"].value() == n["title"].value():
            wiredStyle(n,0)
    elif kn == "title":
        kv = k.value()
        if titleIsLegal(kv):
            if nuke.ask("Do you want to update the linked stamps' title?"):
                a = retitleAnchor(n) # Retitle anchor
                retitleWired(a) # Retitle wired stamps of anchor a
                return
        else:
            nuke.message("Please set a valid title.")
        try:
            n["title"].setValue(n["prev_title"].value())
        except:
            pass
    else:
        try:
            n.knob("toReconnect").setValue(False)
            if ni:
                if isAnchor(n.input(0)):
                    if n.knob("title").value() == n.input(0).knob("title").value():
                        n.knob("anchor").setValue(n.input(0).name())
                    elif nuke.ask("Do you want to change the anchor for the current stamp?"):
                        n.knob("anchor").setValue(n.input(0).name())
                        n.knob("title").setValue(n.input(0).knob("title").value())
                        n.knob("prev_title").setValue(n.input(0).knob("title").value())
                    else:
                        n.setInput(0,None)
        except:
            pass

def anchorKnobChanged():
    k = nuke.thisKnob()
    kn = k.name()
    if kn in ["xpos","ypos"]:
        return
    n = nuke.thisNode()
    if kn == "title":
        kv = k.value()
        if titleIsLegal(kv):
            if nuke.ask("Do you want to update the linked stamps' title?"):
                retitleWired(n) # Retitle wired stamps of anchor a
                #print "Wired stamps retitled"
                return
        else:
            nuke.message("Please set a valid title.")
        try:
            n["title"].setValue(n["prev_title"].value())
        except:
            pass

def retitleAnchor(ref = ""):
    '''
    Retitle Anchor of current wired stamp to match its title.
    returns: anchor node
    ''' 
    if ref == "":
        ref = nuke.thisNode()
    try:
        ref_title = ref["title"].value().strip()
        ref_anchor = ref["anchor"].value()
        na = nuke.toNode(ref_anchor)
        for kn in ["title","prev_title"]:
            na[kn].setValue(ref_title)
        ref["prev_title"].setValue(ref_title)
        return na
    except:
        return None

def retitleWired(anchor = ""):
    '''
    Retitle wired stamps connected to supplied anchor
    '''
    if anchor == "":
        return
    try:
        anchor_title = anchor["title"].value()
        anchor_name = anchor.name()
        for nw in nuke.allNodes("NoOp"):
            if all(nw.knob(i) for i in ["identifier","anchor","title","prev_title"]):
                if nw["identifier"].value() == "wired" and nw["anchor"].value() == anchor_name:
                    nw["title"].setValue(anchor_title)
                    nw["prev_title"].setValue(anchor_title)
        return True
    except:
        pass

def wiredSelectSimilar(anchor_name = ""):
    if anchor_name=="":
        anchor_name = nuke.thisNode().knob("anchor").value()
    for i in nuke.allNodes("NoOp"):
        if i.knob("identifier") and i.knob("anchor"):
            if i.knob("identifier").value() == "wired" and i.knob("anchor").value() == anchor_name:
                i.setSelected(True)

def wiredReconnectSimilar(anchor_name = ""):
    if anchor_name=="":
        anchor_name = nuke.thisNode().knob("anchor").value()
    for i in nuke.allNodes("NoOp"):
        if i.knob("identifier") and i.knob("anchor"):
            if i.knob("identifier").value() == "wired" and i.knob("anchor").value() == anchor_name:
                reconnectErrors = 0
                try:
                    i.knob("reconnect").execute()
                except:
                    reconnectErrors += 1
                finally:
                    if reconnectErrors > 0:
                        nuke.message("Couldn't reconnect {} nodes".format(str(reconnectErrors)))

def anchorReconnectWired(anchor = ""):
    if anchor=="":
        anchor = nuke.thisNode()
    anchor_name = anchor.name()
    for i in nuke.allNodes("NoOp"):
        if i.knob("identifier") and i.knob("anchor"):
            if i.knob("identifier").value() == "wired" and i.knob("anchor").value() == anchor_name:
                reconnectErrors = 0
                try:
                    i.setInput(0,anchor)
                except:
                    reconnectErrors += 1
                finally:
                    if reconnectErrors > 0:
                        nuke.message("Couldn't reconnect {} nodes".format(str(reconnectErrors)))

def wiredZoomNext(anchor_name = ""):
    if anchor_name=="":
        anchor_name = nuke.thisNode().knob("anchor").value()
    anchor = nuke.toNode(anchor_name)
    showing_knob = anchor.knob("showing")
    showing_value = showing_knob.value()
    i = 0
    for ni in nuke.allNodes("NoOp"):
        if ni.knob("identifier") and ni.knob("anchor"):
            if ni.knob("identifier").value() == "wired" and ni.knob("anchor").value() == anchor_name:
                if i == showing_value:
                    nuke.zoom(nuke.zoom(),[ni.xpos(),ni.ypos()])
                    showing_knob.setValue(i+1)
                    return
                i+=1
    showing_knob.setValue(0)
    nuke.message("Couldn't find any more similar wired stamps.")

def showHelp():
    import os
    os.system("firefox http://phabricator.trixter.intern/w/artist/compositing/nuke/enhancements/postage_stamps/ &")

def anchorSelectWireds(anchor = ""):
    if anchor == "":
        try:
            anchor = nuke.selectedNode()
        except:
            pass
    if isAnchor(anchor):
        anchor.setSelected(False)
        wiredSelectSimilar(anchor.name())

wiredOnCreate_code = """if nuke.GUI:
    try:
        nuke.thisNode().knob("toReconnect").setValue(1)
    except:
        pass
"""

wiredReconnectToTitle_code = """n = nuke.thisNode()
try:
    nt = n.knob("title").value()
    for a in nuke.allNodes("NoOp"):
        if a.knob("identifier").value() == "anchor" and a.knob("title").value() == nt:
            n.setInput(0,a)
            break
except:
    nuke.message("Unable to reconnect.")
"""

wiredReconnect_code = """n = nuke.thisNode()
try:
    n.setInput(0,nuke.toNode(n.knob("anchor").value()))
except:
    nuke.message("Unable to reconnect.")
"""

#################################
### STAMP, ANCHOR, WIRED
#################################

def anchor(title = "", tags = "", input_node = "", node_type = "2D"):
    ''' Anchor Stamp '''
    try:
        n = nuke.createNode(StampClasses[node_type])
    except:
        n = nuke.createNode("NoOp")
    n["name"].setValue(getAvailableName("Anchor"))
    # Set default knob values
    defaults = STAMP_DEFAULTS.copy()
    defaults.update(ANCHOR_DEFAULTS)
    for i,j in defaults.items():
        try:
            n.knob(i).setValue(j)
        except:
            pass

    # Main knobs
    anchorTab_knob = nuke.Tab_Knob('anchor_tab','Anchor Stamp')
    identifier_knob = nuke.Text_Knob('identifier','identifier', 'anchor')
    identifier_knob.setVisible(False)
    title_knob = nuke.String_Knob('title','Title', title)
    prev_title_knob = nuke.Text_Knob('prev_title','', title)
    prev_title_knob.setVisible(False)
    showing_knob = nuke.Int_Knob('showing','', 0)
    showing_knob.setVisible(False)
    tags_knob = nuke.String_Knob('tags','Tags', tags)
    for k in [anchorTab_knob, identifier_knob, title_knob, prev_title_knob, showing_knob, tags_knob]:
        n.addKnob(k)

    # Buttons
    wiredLabel_knob = nuke.Text_Knob('wiredLabel','Wired Stamps', "")
    wiredLabel_knob.setFlag(nuke.STARTLINE)
    buttonSelectStamps = nuke.PyScript_Knob("selectStamps","select","import stamps; stamps.wiredSelectSimilar(nuke.thisNode().name())")
    buttonSelectStamps.setFlag(nuke.STARTLINE)
    buttonReconnectStamps = nuke.PyScript_Knob("reconnectStamps","reconnect","import stamps; stamps.anchorReconnectWired()")
    buttonZoomNext = nuke.PyScript_Knob("zoomNext","zoom next","import stamps; stamps.wiredZoomNext(nuke.thisNode().name())")

    for k in [wiredLabel_knob, buttonSelectStamps, buttonReconnectStamps, buttonZoomNext]:
        n.addKnob(k)

    # Version (for future update checks)
    line_knob = nuke.Text_Knob("line", "", "")
    buttonHelp = nuke.PyScript_Knob("buttonHelp","Help","import stamps; stamps.showHelp()")
    version_knob = nuke.Text_Knob('version','',version)
    version_knob.setTooltip(VERSION_TOOLTIP)
    version_knob.clearFlag(nuke.STARTLINE)
    for k in [line_knob, buttonHelp, version_knob]:
        n.addKnob(k)
    n["help"].setValue(STAMPS_HELP)

    return n

def wired(anchor):
    ''' Wired Stamp '''
    global Stamps_LastCreated
    Stamps_LastCreated = anchor.name()
    node_type = nodeType(anchor)
    try:
        n = nuke.createNode(StampClasses[node_type])
    except:
        n = nuke.createNode("NoOp")
    n["name"].setValue(getAvailableName("Stamp"))
    # Set default knob values
    defaults = STAMP_DEFAULTS.copy()
    defaults.update(WIRED_DEFAULTS)
    for i,j in defaults.items():
        try:
            n.knob(i).setValue(j)
        except:
            pass
    n["onCreate"].setValue(wiredOnCreate_code)

    # Main knobs
    wiredTab_knob = nuke.Tab_Knob('wired_tab','Wired Stamp')
    identifier_knob = nuke.Text_Knob('identifier','identifier', 'wired')
    identifier_knob.setVisible(False)
    toReconnect_knob = nuke.Boolean_Knob("toReconnect")
    toReconnect_knob.setVisible(False)
    title_knob = nuke.String_Knob('title','Title', anchor["title"].value())
    prev_title_knob = nuke.Text_Knob('prev_title','', anchor["title"].value())
    prev_title_knob.setVisible(False)
    anchor_knob = nuke.String_Knob('anchor','Anchor', anchor.name())

    for k in [wiredTab_knob, identifier_knob, toReconnect_knob, title_knob, prev_title_knob, anchor_knob]:
        n.addKnob(k)

    wiredTab_knob.setFlag(0) #Open the tab

    # Buttons
    anchorLabel_knob = nuke.Text_Knob('anchorLabel','Anchor Stamp', "")
    anchorLabel_knob.setFlag(nuke.STARTLINE)
    buttonShow = nuke.PyScript_Knob("show","show","import stamps; stamps.wiredShowAnchor()")
    buttonShow.clearFlag(nuke.STARTLINE)
    buttonZoomAnchor = nuke.PyScript_Knob("zoomAnchor","zoom","import stamps; stamps.wiredZoomAnchor()")
    buttonReconnect = nuke.PyScript_Knob("reconnect","reconnect",wiredReconnect_code)

    wiredLabel_knob = nuke.Text_Knob('wiredLabel','Wired Stamps', "")
    wiredLabel_knob.setFlag(nuke.STARTLINE)
    buttonSelectSimilar = nuke.PyScript_Knob("selectSimilar","select similar","import stamps; stamps.wiredSelectSimilar()")
    buttonSelectSimilar.setFlag(nuke.STARTLINE)
    buttonZoomNext = nuke.PyScript_Knob("zoomNext","zoom next","import stamps; stamps.wiredZoomNext()")
    buttonReconnectSimilar = nuke.PyScript_Knob("reconnectSimilar","reconnect similar","import stamps; stamps.wiredReconnectSimilar()")

    for k in [anchorLabel_knob, buttonShow, buttonZoomAnchor, buttonReconnect, wiredLabel_knob, buttonSelectSimilar, buttonZoomNext, buttonReconnectSimilar]:
        n.addKnob(k)

    # Version (for future update checks)
    line_knob = nuke.Text_Knob("line", "", "")
    buttonHelp = nuke.PyScript_Knob("buttonHelp","Help","import stamps; stamps.showHelp()")
    version_knob = nuke.Text_Knob('version','',version)
    version_knob.clearFlag(nuke.STARTLINE)
    version_knob.setTooltip(VERSION_TOOLTIP)
    for k in [line_knob, buttonHelp, version_knob]:
        n.addKnob(k)

    # Hide input while not messing possition
    x,y = n.xpos(),n.ypos()
    n.setInput(0,anchor)
    n["hide_input"].setValue(True)
    n["xpos"].setValue(x)
    n["ypos"].setValue(y)

    n["help"].setValue(STAMPS_HELP)

    return n
    Stamps_LastCreated = anchor.name()

def getAvailableName(name = "Untitled"):
    ''' Returns a node name starting with @name followed by a number, that doesn't exist already '''
    i = 1
    while True:
        available_name = name+str(i)
        if not nuke.exists(available_name):
            return available_name
        i += 1

#################################
### ANCHOR SELECTION CLASS
#################################

class AnchorSelector(QtWidgets.QDialog):
    '''
    Panel to select an anchor, showing the different anchors on dropdowns based on their tags.
    '''
    def __init__(self):
        super(AnchorSelector, self).__init__()
        self.setWindowTitle("Select an anchor.")
        self.initUI()
        self.custom_anchors_lineEdit.setFocus()

    def initUI(self):
        # Find all anchors and get all tags
        self.findAnchorsAndTags() # Generate a dictionary: {"Camera1":["Camera","New","Custom1"],"Read":["2D","New"]}
        self.custom_chosen = False # If clicked OK on the custom lineedit

        # Layouts
        self.master_layout = QtWidgets.QVBoxLayout()
        self.grid = QtWidgets.QGridLayout()

        for tag_num, tag in enumerate(self._all_tags):
            if tag == "":
                continue
            tag_label = QtWidgets.QLabel(tag+": ")
            tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            anchors_dropdown = QtWidgets.QComboBox()
            for i, cur_name in enumerate(self._all_anchors_names):
                cur_title = self._all_anchors_titles[i]
                ##title_repeated = self._all_anchors_titles.count(cur_title) #TODO: repeated for current tag, not just anywhere (function already started)
                title_repeated = self.titleRepeatedForTag(cur_title, tag)
                if tag in self._anchors_and_tags[cur_name]:
                    if title_repeated:
                        anchors_dropdown.addItem("{0} ({1})".format(cur_title, cur_name), cur_name)
                    else:
                        anchors_dropdown.addItem(cur_title, cur_name)

            ok_btn = QtWidgets.QPushButton("OK")
            ok_btn.clicked.connect(partial(self.okPressed,dropdown=anchors_dropdown))

            self.grid.addWidget(tag_label,tag_num,0)
            self.grid.addWidget(anchors_dropdown,tag_num,1)
            self.grid.addWidget(ok_btn,tag_num,2)

        # ALL
        tag_num = len(self._all_tags)
        all_tag_label = QtWidgets.QLabel("<b>all</b>: ")
        all_tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.all_anchors_dropdown = QtWidgets.QComboBox()

        all_tag_texts = [] # List of all texts of the items (usually equals the "title", or "title (name)")
        all_tag_names = [i for i in self._all_anchors_names] # List of all real anchor names of the items.
        for i, cur_name in enumerate(self._all_anchors_names):
            cur_title = self._all_anchors_titles[i]
            title_repeated = self._all_anchors_titles.count(cur_title)
            if title_repeated > 1:
                all_tag_texts.append("{0} ({1})".format(cur_title, cur_name))
            else:
                all_tag_texts.append(cur_title)
        self.all_tag_sorted = sorted(zip(all_tag_texts,all_tag_names),  key=lambda pair: pair[0].lower())

        for [text, name] in self.all_tag_sorted:
            self.all_anchors_dropdown.addItem(text, name)

        all_ok_btn = QtWidgets.QPushButton("OK")
        all_ok_btn.clicked.connect(partial(self.okPressed,dropdown=self.all_anchors_dropdown))
        self.grid.addWidget(all_tag_label,tag_num,0)
        self.grid.addWidget(self.all_anchors_dropdown,tag_num,1)
        self.grid.addWidget(all_ok_btn,tag_num,2)
        tag_num += 1

        # LineEdit with completer
        custom_tag_label = QtWidgets.QLabel("<b>by title</b>: ")
        custom_tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.custom_anchors_lineEdit = QtWidgets.QLineEdit()
        self.custom_anchors_completer = QtWidgets.QCompleter([i for i,_ in self.all_tag_sorted], self)
        self.custom_anchors_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.custom_anchors_completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        self.custom_anchors_lineEdit.setCompleter(self.custom_anchors_completer)

        custom_ok_btn = QtWidgets.QPushButton("OK")
        custom_ok_btn.clicked.connect(partial(self.okCustomPressed,dropdown=self.custom_anchors_lineEdit))
        self.grid.addWidget(custom_tag_label,tag_num,0)
        self.grid.addWidget(self.custom_anchors_lineEdit,tag_num,1)
        self.grid.addWidget(custom_ok_btn,tag_num,2)

        # Layout shit
        self.grid.setColumnStretch(1,1)
        self.master_layout.addLayout(self.grid)
        self.setLayout(self.master_layout)

    def keyPressEvent(self, e):
        selectorType = type(self.focusWidget()).__name__ #QComboBox or QLineEdit
        if e.key() == 16777220:
            if selectorType == "QLineEdit":
                self.okCustomPressed(dropdown=self.focusWidget())
            else:
                self.okPressed(dropdown=self.focusWidget())
        else:
            return QtWidgets.QDialog.keyPressEvent(self, e)

    def findAnchorsAndTags(self):
        # Lets find anchors
        self._all_anchors_titles = []
        self._all_anchors_names = []
        self._all_tags = set()
        self._anchors_and_tags = {} # Name:tags. Not title.
        for ni in nuke.allNodes("NoOp"):
            if ni.knob("identifier") and ni.knob("identifier").value() == "anchor":
                try:
                    title_value = ni["title"].value()
                    name_value = ni.name()
                    tags_value = ni["tags"].value()
                    tags = re.split(" *, *",tags_value.strip()) # Remove leading/trailing spaces and separate by commas (with or without spaces)
                    self._all_anchors_titles.append(title_value.strip())
                    self._all_anchors_names.append(name_value)
                    self._all_tags.update(tags)
                    self._anchors_and_tags[name_value] = set(tags)
                except:
                    pass
        return self._anchors_and_tags

    def titleRepeatedForTag(self, title, tag):
        # DONE IT SEEMS!!!!! NOW IMPLEMENT.
        if self._all_anchors_titles.count(title) <= 1:
            return False

        # Get list of all names that have that tag, and list of related titles
        names_with_tag = []
        titles_with_tag = []
        for i, name in enumerate(self._all_anchors_names):
            if tag in self._anchors_and_tags[name]:
                names_with_tag.append(name)
                titles_with_tag.append(self._all_anchors_titles[i])

        # Count titles repetition
        title_repetitions = titles_with_tag.count(title)
        return (title_repetitions > 1)


    def okPressed(self, dropdown):
        ''' Runs after an ok button is pressed '''
        dropdown_value = dropdown.currentText()
        dropdown_index = dropdown.currentIndex()
        dropdown_data = dropdown.itemData(dropdown_index)

        try:
            match_anchor = nuke.toNode(dropdown_data)
        except:
            pass

        self.chosen_value = dropdown_value
        self.chosen_anchor_name = dropdown_data
        if match_anchor is not None:
            self.chosen_anchor = match_anchor
            self.accept()
        else:
            nuke.message("There was a problem selecting a valid anchor.")

    def okCustomPressed(self, dropdown):
        ''' Runs after the custom ok button is pressed '''
        global Stamps_LastCreated
        written_value = dropdown.text() # This means it's been written down on the lineEdit
        written_lower = written_value.lower().strip()

        found_data = None

        if written_value == "" and globals().has_key('Stamps_LastCreated'):
            found_data = Stamps_LastCreated
        else:
            for [text, name] in self.all_tag_sorted:
                if written_lower in text.lower():
                    found_data = name
                    break
        try:
            match_anchor = nuke.toNode(found_data)
        except:
            nuke.message("Please write a valid name.")
            return

        self.chosen_value = written_value
        self.chosen_anchor_name = found_data
        if match_anchor is not None:
            self.chosen_anchor = match_anchor
            self.accept()
        else:
            nuke.message("There was a problem selecting a valid anchor.")

#################################
### FUNCTIONS
#################################

def getDefaultTitle(node = None):
    if node == None:
        return False
    title = str(node.name())
    if "tx_edit_format" in title:
        title = "editRef"
        return title

    # If cam
    if "Camera" in node.Class() and not any([(i.knob("title") and i["title"].value() == "cam") for i in nuke.allNodes("NoOp")]):
        title = "cam"
        return title

    # If filename
    try:
        file = node['file'].value()
        if not (node.knob("read_from_file") and not node["read_from_file"].value()):
            if file != "":
                rawname = file.rpartition('/')[2].rpartition('.')[0]
                if '.' in rawname:
                    rawname = rawname.rpartition('.')[0]
                # 1: beauty?
                m = re.match(r"([\w]+)_v[\d]+_beauty", rawname)
                if m:
                    pre_version = m.groups()[0]
                    title = "_".join(pre_version.split("_")[3:])
                    return title
                # 2: Other
                rawname = str(re.split("_v[0-9]*_",rawname)[-1]).replace("_render","")
                title = rawname
    except:
        pass

    # If element
    try: 
        title = selNode['element'].value()
    except:
        pass

    return title

def stampCreateAnchor(node = None, extra_tags = [], no_default_tag = False):
    '''
    Create a stamp from any nuke node.
    Returns: extra_tags list is success, None if cancelled
    '''
    ns = nuke.selectedNodes()
    for n in ns:
        n.setSelected(False)

    if node is not None:
        node.setSelected(True)
        default_title = getDefaultTitle(node)
        default_tag = nodeType(node)
        node_type = nodeType(node)
        window_title = "New Stamp: "+str(node.name())
    else:
        default_title = ""
        default_tag = ""
        node_type = "2D"
        window_title = "New Stamp"

    panel = nuke.Panel(window_title)
    panel.setWidth(240)
    panel.addSingleLineInput("Title:",default_title)
    if no_default_tag:
        default_tags = ", ".join(extra_tags)
    else:
        default_tags = default_tag + ", " + ", ".join(extra_tags)
    panel.addSingleLineInput("Tags:",default_tags)

    while True:
        if panel.show():
            anchor_title = panel.value("Title:").strip()
            anchor_tags = panel.value("Tags:")
            if not titleIsLegal(anchor_title):
                nuke.message("Please set a valid title.")
                continue
            elif len(findAnchorsByTitle(anchor_title)):
                if not nuke.ask("There is already a Stamp titled "+anchor_title+".\nDo you still want to use this title?"):
                    continue
            na = anchor(title = anchor_title, tags = anchor_tags, input_node = node, node_type = node_type)
            na.setYpos(na.ypos()+20)
            stampCreateWired(na)
            for n in ns:
                n.setSelected(True)
                node.setSelected(False)
            extra_tags = re.split(" *, *",anchor_tags.strip())
            extra_tags = [t for t in extra_tags if t != default_tag]
            break
        else:
            break
        
    return extra_tags

def stampSelectAnchor():
    '''
    Panel to select a stamp anchor (if there are any)
    Returns: selected anchor node, or None.
    '''
    # 1.Get position where to make the child...
    nodeForPos = nuke.createNode("NoOp")
    childNodePos = [nodeForPos.xpos(),nodeForPos.ypos()]
    nuke.delete(nodeForPos)
    # 2.Choose the anchor...
    anchorList = [n.name() for n in nuke.allNodes("NoOp") if n.knob("identifier") and n["identifier"].value() == "anchor"]
    if not len(anchorList):
        nuke.message("Please create some stamps first...")
        return None
    else:
        # REDONE ON THE NEXT LINES
        global select_anchor_panel
        select_anchor_panel = AnchorSelector()
        if select_anchor_panel.exec_(): # If user clicks OK
            chosen_anchor = select_anchor_panel.chosen_anchor
            #all_anchors_dropdown_list = select_anchor_panel.all_anchors_dropdown_list #TODO
            if chosen_anchor:
                return chosen_anchor
        return None

def stampCreateWired(anchor = ""):
    ''' Create a wired stamp from an anchor node. '''
    global Stamps_LastCreated
    if anchor == "":
        anchor = stampSelectAnchor()
        if anchor == None:
            return
        nw = wired(anchor = anchor)
        nw.setInput(0,anchor)
    else:
        ns = nuke.selectedNodes()
        for n in ns:
            n.setSelected(False)
        dot = nuke.nodes.Dot()
        dot.setXYpos(anchor.xpos(),anchor.ypos())
        dot.setInput(0,anchor)
        #anchor.setSelected(True)
        nw = wired(anchor = anchor)
        nw.setXYpos(anchor.xpos(),anchor.ypos()+56)
        nuke.delete(dot)
        for n in ns:
            n.setSelected(True)
        anchor.setSelected(False)
    return nw

def stampDuplicateWired(wired = ""):
    ''' Create a duplicate of a wired stamp '''
    ns = nuke.selectedNodes()
    for n in ns:
        n.setSelected(False)
    wired.setSelected(True)

    clipboard = QtWidgets.QApplication.clipboard()
    ctext = clipboard.text()
    nuke.nodeCopy("%clipboard%")
    wired.setSelected(False)
    new_wired = nuke.nodePaste("%clipboard%")
    clipboard.setText(ctext)
    new_wired.setXYpos(wired.xpos()-110,wired.ypos()+55)
    try:
        new_wired.setInput(0,wired.input(0))
    except:
        pass
    for n in ns:
        n.setSelected(True)
    wired.setSelected(False)

def stampType(n = ""):
    ''' Returns the identifier value if it exists, otherwise False. '''
    stamp_id_knob = n.knob("identifier") # Could be anchor, or wired
    if isAnchor(n):
        return "anchor"
    elif isWired(n):
        return "wired"
    else:
        return False

def nodeType(n=""):
    '''Returns the node type: Camera, Deep, 3D, Particles, Image or False'''
    try:
        nodeClass = n.Class()
    except:
        return False
    if nodeClass.startswith("Deep") and nodeClass not in DeepExceptionClasses:
        return "Deep"
    elif nodeClass.startswith("Particle") and nodeClass not in ParticleExceptionClasses:
        return "Particle"
    elif nodeClass in ["Camera", "Camera2"]:
        return "Camera"
    elif (n.knob("render_mode") and n.knob("display")) or nodeClass in ["Axis2"]:
        return "3D"
    else:
        return "2D"

def totalAnchors(selection=""):
    if selection == "":
        selection = nuke.allNodes("NoOp")
    num_anchors = len([a for a in selection if a in nuke.allNodes("NoOp") and a.knob("title") and a.knob("identifier") and a["identifier"].value() == "anchor"])
    return num_anchors

def findAnchorsByTitle(title = "", selection=""):
    ''' Returns list of nodes '''
    if title == "":
        return None
    if selection == "":
        found_anchors = [a for a in nuke.allNodes("NoOp") 
                            if a.knob("identifier") and a["identifier"].value() == "anchor"
                            and a.knob("title") and a.knob("title").value() == title]
    else:
        found_anchors = [a for a in selection if a in nuke.allNodes("NoOp")
                            and a.knob("identifier") and a["identifier"].value() == "anchor"
                            and a.knob("title") and a.knob("title").value() == title]
    return found_anchors

def titleIsLegal(title=""):
    '''
    Convenience function to determine which stamp titles are legal.
    titleIsLegal(title) -> True or False
    '''
    if not title or title == "":
        return False
    return True

def isAnchor(node=""):
    ''' True or False '''
    return True if all(node.knob(i) for i in ["identifier","title"]) and node["identifier"].value() == "anchor" else False
        
def isWired(node=""):
    ''' True or False '''
    return True if all(node.knob(i) for i in ["identifier","title"]) and node["identifier"].value() == "wired" else False


#################################
### MAIN IMPLEMENTATION
#################################

def goStamp(ns=""):
    ''' Main stamp function, the one that is called when pressing the main shortcut. '''
    if ns=="":
        ns = nuke.selectedNodes()
    if not len(ns):
        if not totalAnchors(): # If no anchors on the script, create an anchor with no input
            stampCreateAnchor(no_default_tag = True)
        else:
            stampCreateWired() # Selection panel in order to create a stamp
            return
    else:
        # Warn if the selection is too big
        if len(ns) > 10 and not nuke.ask("You have "+str(len(ns))+" nodes selected.\nDo you want make stamps for all of them?"):
            return
        # Main loop
        extra_tags = []
        for n in ns:
            if isAnchor(n):
                # Make a child to n
                stampCreateWired(n)
            elif isWired(n):
                # Make a copy of n next to it
                stampDuplicateWired(n)
            else:
                if n.knob("stamp_tags"):
                    stampCreateAnchor(n, extra_tags = n.knob("stamp_tags").value().split(","), no_default_tag = True)
                else:
                    extra_tags = stampCreateAnchor(n, extra_tags = extra_tags) # Create anchor via anchor creation panel
                if "Cryptomatte" in n.Class() and n.knob("matteOnly"):
                    n['matteOnly'].setValue(1)

stShortcut = "shift+F8" # TO CHANGE FOR F8
nuke.menu('Nuke').addCommand('Edit/Stamps/Make Stamp', 'reload(stamps);stamps.goStamp()', stShortcut)