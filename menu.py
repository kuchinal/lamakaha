import nuke
import nukescripts
import os
#


#######
UserDir = "/home/alexey/Dropbox/users/underUserAlexey/"
n11,n10 = False,True
if nuke.NUKE_VERSION_MAJOR > 10:
    n11 = True;n10 = False

    
#gfgfg

nuke.tprint("_"*100);nuke.tprint("now loading my user");nuke.tprint("_"*100);nuke.tprint("_"*100)


import knob_scripter
import mps3

#test

import TrackToRoto
import autoBackdropp
import Dots
import Label
import shuffle_Smart
import getTheCornerpinAsMatrix
import cornerMatrixToPaint
import autoSticky
import myTransform
import myCC
import myMerge
import copyFileName
import copyConnected
import Explorer
import Hidden
import inverter
import W_scaleTree
import stamps

########animated snap########################################################
import animatedSnap3D
from animatedSnap3D import *
# Add menu items under the Axis Menu
try:
    m = nuke.menu('Axis').findItem('Snap')
    m.addSeparator()
    m.addCommand('Match position - ANIMATED', 'animatedSnap3D.translateThisNodeToPointsAnimated()')
    m.addCommand('Match position, orientation - ANIMATED', 'animatedSnap3D.translateRotateThisNodeToPointsAnimated()')
    m.addCommand('Match position, orientation, scale - ANIMATED', 'animatedSnap3D.translateRotateScaleThisNodeToPointsAnimated()')

except:
    pass

#setting knob defaultsq
import knobDefaults 
knobDefaults.knobDefaults()




nukeMenu = nuke.menu( 'Nuke' ).addMenu("HOME",icon = "nuke.png")
t=nukeMenu.addMenu("tmp")
t.addCommand( 'show review notes', 'reviews.reviews()')
t.addCommand("Copy file to the clipboard! ", "copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")

viewerMenu = nuke.menu('Viewer')
viewerMenu.addCommand("saveImage", "saveImage.saveImage()")

animationMenu = nuke.menu('Animation')
animationMenu.addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')


nodegraphMenu = nuke.menu('Node Graph')
#t=nukeMenu.addMenu("shortcuted")
nodegraphMenu.addCommand('TrackToRoto','TrackToRoto.RotoFromTrack()',"Shift+p",icon="Tracker.png")
nodegraphMenu.addCommand('Auto Backdrop', 'autoBackdropp.autoBackdrop()', 'alt+b',icon = "Backdrop.png")
nodegraphMenu.addCommand('Auto Sticky', 'autoSticky.autoSticky()', 'alt+n',icon = "Backdrop.png")
nodegraphMenu.addCommand("Copy file names", "copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")
nodegraphMenu.addCommand('Dots ', 'Dots.Dots()', ',',icon = "Dot.png")
nodegraphMenu.addCommand('Open Read in File Browser', 'Explorer.ExplorerJPEG()',"Alt+Shift+r",icon = "Explorer.png")
nodegraphMenu.addCommand('HiddenPostages Toggle visibility','stamps.anchorSelectWireds()', "z",icon = "PostageStamp.png")
nodegraphMenu.addCommand('W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
nodegraphMenu.addCommand("Create inverted axis from curent axis ", "inverter.inverter()",icon = "Axis.png")
nodegraphMenu.addCommand('Shortcuted/@;Label', 'Label.Label()',"n",icon = "Label.png")
nodegraphMenu.addCommand('Transform', 'myTransform.transformThis()', 't')
nodegraphMenu.addCommand( 'Merge', 'myMerge.mergeThis()', 'm')
nodegraphMenu.addCommand("MyCC", "myCC.myCC()","c")
nodegraphMenu.addCommand('Paste To Selected', 'pasteToSelected.pasteToSelected()',"Alt+f5", index=10,icon="my.png")
nodegraphMenu.addCommand('Stamp', 'stamps.goStamp()', "F8",icon = "PostageStamp.png")



#on create stuff
#code for wild card stuff
def wCard():
    if nuke.NUKE_VERSION_MAJOR < 11:
        import PySide
    else:
        import PySide2
    node = nuke.thisNode()
    from cryptomatte_utilities import CryptomatteInfo
    current_layer = CryptomatteInfo(node).selection
    clipboard = PySide2.QtGui.QGuiApplication.clipboard()
    wildcard = clipboard.text()
    #wildcard = node['WildnessLevel'].value()
    in_list = []
    manifest = json.loads(node.metadata("exr/cryptomatte/{0}/manifest".format(current_layer) ))
    for m in manifest.keys():
        if str(m).find(wildcard.
            rstrip("*")) != -1:
            if str(m) not in in_list:
                in_list.append(str(m))
    out_list = ", ".join(in_list)
    node.knob("matteList").setValue(out_list)
    print "script by Marco Meyer"
def WildCardButton():
    w = nuke.Text_Knob("W","")
    m = nuke.PyScript_Knob("wildCard","Wild card","wCard()")
    #t = nuke.String_Knob("WildnessLevel","Wildness Level")
    h = nuke.Text_Knob("help","Wild help","\n\n\n1 pick one of objects you want to get with Picker\n2 Manually copy the string from 'Matte List' up to area you do not want to have\n3 press 'Wild Card' button!\n----------------------------\n\n\n Example:\nroot/human/arm/wrist/fingers/fingerA\n If you want to get all the fingers copy:\nroot/human/arm/wrist/fingers/")
    n=nuke.thisNode()
    try:
        n['W']
        pass
    except Exception:
        n.addKnob(w)
        n.addKnob(m)
        #n.addKnob(t)
        n.addKnob(h)
nuke.addOnCreate(lambda: WildCardButton() , nodeClass="Cryptomatte")





nuke.tprint("_"*100);nuke.tprint("my user is loaded");nuke.tprint("_"*100)

#finished to bring stuff from underuser, have to start to dig into my trx user













































nuke.tprint("_"*100);nuke.tprint("my user loaded");nuke.tprint("_"*100)
