import nuke
import nukescripts
import os

UserDir = "/home/alexey/Dropbox/users/underUserAlexey/"
n11,n10 = False,True
if nuke.NUKE_VERSION_MAJOR > 10:
    n11 = True;n10 = False

    


nuke.tprint("_"*100);nuke.tprint("now loading my user");nuke.tprint("_"*100);nuke.tprint("_"*100)


import knob_scripter
import mps3


import TrackToRoto
import autoBackdropp
import Dots
import Label
import NameMy
import shuffle_Smart
import getTheCornerpinAsMatrix
import cornerMatrixToPaint
import autoSticky
import myTransform
import myCC
import myMerge
import saveImage
import reviews
import copyFileName




#temporary
def RotoFromTrack():
    try:
        a = nuke.selectedNode()
        if "Tracker" in a.Class():
            TrackToRoto.TrackToRoto()
        elif "CornerPin" in a.Class() or "CornerPin" in a['name'].value():
            getTheCornerpinAsMatrix.getTheCornerpinAsMatrix();cornerMatrixToPaint.cornerMatrixToPaint()
        else:
            nuke.createNode("Roto")
    except:
        import traceback; traceback.print_exc()
        nuke.createNode("Roto") 





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





nukeMenu = nuke.menu( 'Nuke' ).addMenu("HOME",icon = "nuke.png")
t=nukeMenu.addMenu("tmp")
t.addCommand( 'show review notes', 'reviews.reviews()')
t.addCommand("Copy file to the clipboard! ", "copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")

viewerMenu = nuke.menu('Viewer')
viewerMenu.addCommand("saveImage", "saveImage.saveImage()")

animationMenu = nuke.menu('Animation')
animationMenu.addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')

nodegraphMenu = nuke.menu('Node Graph')
t=nukeMenu.addMenu("shortcuted")
nodegraphMenu.addCommand('TrackToRoto','RotoFromTrack()',"Shift+p",icon="Tracker.png")
nodegraphMenu.addCommand('Auto Backdrop', 'autoBackdropp.autoBackdrop()', 'alt+b',icon = "Backdrop.png")








nuke.tprint("_"*100);nuke.tprint("my user is loaded");nuke.tprint("_"*100)














































nuke.tprint("_"*100);nuke.tprint("my user loaded");nuke.tprint("_"*100)
