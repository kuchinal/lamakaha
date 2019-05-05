import nuke
import nukescripts
import os


nMajor = nuke.NUKE_VERSION_MAJOR

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


















































nuke.tprint("_"*100);nuke.tprint("my user loaded");nuke.tprint("_"*100)
