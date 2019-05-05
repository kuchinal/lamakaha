import nuke
import nukescripts
import os

UserDir = "/home/alexey/Dropbox/users/underUserAlexey/"
n11,n10 = False,True
if nuke.NUKE_VERSION_MAJOR > 10:
    n11 = True;n10 = False

    

nuke.tprint("_"*100);nuke.tprint("now loading my user");nuke.tprint("_"*100)


import KnobScripter
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




#nuke.menu( 'Node Graph' ).addCommand( 'localize Threaded', 'LocaliseThreaded.locCode()')

n = nuke.menu( 'Nuke' ).addMenu("HOME",icon = "nuke.png")
t=n.addMenu("tmp")
t.addCommand( 'show review notes', 'reviews.reviews()')
#FIX  t.addCommand("Copy file to the clipboard! ", "copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")


m = nuke.menu('Viewer')
m.addCommand("saveImage", "saveImage.saveImage()")

a = nuke.menu('Animation')
a.addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')
















































nuke.tprint("_"*100);nuke.tprint("my user loaded");nuke.tprint("_"*100)
