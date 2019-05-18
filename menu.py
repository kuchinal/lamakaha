import nuke
import nukescripts
import os
#


#######
UserDir = os.path.dirname(__file__)

n11,n10 = False,True
if nuke.NUKE_VERSION_MAJOR > 10:
    n11 = True;n10 = False

    
#gfgfg

nuke.tprint("_"*100);nuke.tprint("now loading my user");nuke.tprint("_"*100);nuke.tprint("_"*100)


import knob_scripter
import mps3

import Dots
import Label

import myTransform
import myCC
import myMerge

import copyConnected



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

#setting knob defaults
import knobDefaults 
knobDefaults.knobDefaults()

#on create stuff
import onCreateFunctions
onCreateFunctions.onCreateFunctions()


nukeMenu = nuke.menu( 'Nuke' ).addMenu("HOME",icon = "nuke.png")
t=nukeMenu.addMenu("tmp")

viewerMenu = nuke.menu('Viewer')
viewerMenu.addCommand("saveImage", "import saveImage; saveImage.saveImage()")

animationMenu = nuke.menu('Animation')
animationMenu.addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')


nodegraphMenu = nuke.menu('Node Graph')
#t=nukeMenu.addMenu("shortcuted")
nodegraphMenu.addCommand('TrackToRoto','import TrackToRoto; TrackToRoto.RotoFromTrack()',"Shift+p",icon="Tracker.png")
nodegraphMenu.addCommand('Auto Backdrop', 'import autoBackdropp; autoBackdropp.autoBackdrop()', 'alt+b',icon = "Backdrop.png")
nodegraphMenu.addCommand('Auto Sticky', 'import autoSticky; autoSticky.autoSticky()', 'alt+n',icon = "Backdrop.png")
nodegraphMenu.addCommand("Copy file names", "import copyFileName; copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")
nodegraphMenu.addCommand('Dots ', 'Dots.Dots()', ',',icon = "Dot.png")
nodegraphMenu.addCommand('Open Read in File Browser', 'import Explorer; Explorer.ExplorerJPEG()',"Alt+Shift+r",icon = "Explorer.png")
nodegraphMenu.addCommand('HiddenPostages Toggle visibility','stamps.anchorSelectWireds()', "z",icon = "PostageStamp.png")
nodegraphMenu.addCommand('W_scaleTree', 'import W_scaleTree; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
nodegraphMenu.addCommand("Create inverted axis from curent axis ", "import inverter; inverter.inverter()",icon = "Axis.png")
nodegraphMenu.addCommand('Shortcuted/@;Label', 'Label.Label()',"n",icon = "Label.png")
nodegraphMenu.addCommand('Transform', 'myTransform.transformThis()', 't')
nodegraphMenu.addCommand('Merge', 'myMerge.mergeThis()', 'm',shortcutContext=2)
nodegraphMenu.addCommand("MyCC", "myCC.myCC()","c")
nodegraphMenu.addCommand('Paste To Selected', 'pasteToSelected.pasteToSelected()',"Alt+f5", index=10,icon="my.png")
nodegraphMenu.addCommand('Stamp', 'stamps.goStamp()', "F8",icon = "PostageStamp.png")
nodegraphMenu.addCommand("Filter/Channel Blur","nuke.createNode(\'ChannelBlur\')",icon = "Blur.png")
nodegraphMenu.addCommand("Filter/Lens Kernel","nuke.createNode(\'LensKernel\')",icon = "Blur.png")
nodegraphMenu.addCommand("Filter/Filler","nuke.createNode(\'Filler\')",icon = "Blur.png")
nodegraphMenu.addCommand('Filter/EdgeScatter', "nuke.createNode(\"EdgeScatter\")",icon = "Defocus.png")
nodegraphMenu.addCommand("Filter/VoronoiGradient","nuke.createNode(\'VoronoiGradient\')",icon = "Ramp.png")
nodegraphMenu.addCommand('Transform/CardToTrack', "nuke.createNode(\"CardToTrack\")",icon = "Card.png")
nodegraphMenu.addCommand("ErodeMini", "nuke.createNode(\'ErodeMini\')", "e", icon="Erode.png")
nodegraphMenu.addCommand("Exponential Glow My", "nuke.createNode(\'Eglow\')","Shift+g",icon="Glow.png")
nodegraphMenu.addCommand("Fresnel ", "nuke.createNode(\'Fresnel\')", icon="Wireframe.png")
nodegraphMenu.addCommand("MotionBlurCurved ", "nuke.createNode(\'MotionBlurCurved\')",icon ="MotionBlur2D.png")
nodegraphMenu.addCommand("PerspectiveGuide", "nuke.createNode('BB_PerspectiveGuide_1_1_0')", icon="BB_icon.png")
nodegraphMenu.addCommand("Rough Edge-", "nuke.createNode(\'RoughEdgeMy\')")
nodegraphMenu.addCommand("Filter/DarkWrap","nuke.createNode(\'DarkWrap\')",icon = "Blur.png")
nodegraphMenu.addCommand("Copy file to the clipboard! ", "copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")
nodegraphMenu.addCommand('Preferences override','import preferencesOverride; preferencesOverride.preferencesOverride()')
nodegraphMenu.addCommand("ContactSheetMy", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ContactSheetMy.nk')")
nodegraphMenu.addCommand("Find Pigs", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/findPigs.nk')")
nodegraphMenu.addCommand("Start Trmplate", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/StartTemplate.nk')")
nodegraphMenu.addCommand("Review", "import review; review.review()","F9", icon="my.png")
#nodegraphMenu.addCommand('Align/autoplace', 'autoplace()',"Ctrl+Alt+l")
nodegraphMenu.addCommand('Align/vertically', 'import alignNodes; alignNodes.alignNodes( nuke.selectedNodes(), direction="x" )',"Ctrl+l")
nodegraphMenu.addCommand("Backdrops/Fix Layering", "import backdropTools; backdropTools.fixBackdropDepth()")
nodegraphMenu.addCommand("UV generator", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/UVgenerator.nk')",icon="UVv.png")
nodegraphMenu.addCommand("VolumeRays", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/VolumeRays.nk')", icon="Ramp.png")
nodegraphMenu.addCommand("Difference", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Difference.nk')", icon="my.png")  
nodegraphMenu.addCommand("Caustic", "nuke.createNode(\'Caustics\')") 
nodegraphMenu.addCommand("ChromAbb",  "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ChromAbb.nk')", icon="FlareFactoryPlus.png")
nodegraphMenu.addCommand('concatenate2Dtransforms','importconcatenate2Dtransforms; concatenate2Dtransforms.transformstoMatrix()',icon="Tracker.png")
nodegraphMenu.addCommand('Smoother','import  Smoother; Smoother.Smoother()') 
nodegraphMenu.addCommand("Offset", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Offset.nk')", icon="my.png")
nodegraphMenu.addCommand("ITransform","nuke.nodePaste(UserDir+'/Folders/NukeScripts/iTransform.nk')","Alt+f3", icon="my.png")
nodegraphMenu.addCommand('Paste To Selected', 'import pasteToSelected; pasteToSelected.pasteToSelected()',"Alt+f5", index=10,icon="my.png")
nodegraphMenu.addCommand('getColor','import getColor; getColor.getColor()',icon="my.png")
nodegraphMenu.addCommand("Full Fade", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/FullFade.nk')","Shift+f",icon="my.png")       
nodegraphMenu.addCommand("PolarCoordinates", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/PolarCoordinates.nk')",icon="my.png")
nodegraphMenu.addCommand("Rest/Expression", "import expressionMy; expressionMy.expressionMy()","Alt+f1", icon="my.png")
nodegraphMenu.addCommand("shuffle/shuffleRed",'import shuffle_Smart;shuffle_Smart.shuffleRed()',"r")
nodegraphMenu.addCommand("shuffle/shuffleAlpha",'import shuffle_Smart;shuffle_Smart.shuffleAlpha()',"a")
nodegraphMenu.addCommand("shuffle/shuffleBlue",'import shuffle_Smart;shuffle_Smart.shuffleBlue()',"b")
nodegraphMenu.addCommand("shuffle/shuffleGreen",'import shuffle_Smart;shuffle_Smart.shuffleGreen()',"g")
nodegraphMenu.addCommand("Rest/shuffleCreate",'import shuffle_Smart;shuffle_Smart.shuffleCreate()',"s")
nodegraphMenu.addCommand("Rest/shuffleDepth",'import shuffle_Smart;shuffle_Smart.shuffleDepth()',"d")
nodegraphMenu.addCommand('Rest/Invert', "nuke.createNode(\"Invert\")","i",icon="my.png")       
nodegraphMenu.addCommand("Multiply", "fademult;fademult.fademult()","f", icon="ColorMath.png")
nodegraphMenu.addCommand("HueCorrect", "nuke.createNode(\"HueCorrect\")","h", icon="HueCorrect.png")
nodegraphMenu.addCommand("Shortcuted/Splay First", "nuke.splayNodes(False, False)", "Down")
nodegraphMenu.addCommand("Shortcuted/Connect", "nuke.connectNodes(False, False)", "Up")
nodegraphMenu.addCommand('Align/horizontally', 'import alignNodes; alignNodes.alignNodes( nuke.selectedNodes(), direction="y" )',"l")
nodegraphMenu.addCommand("scaleNodesExpand", "import scaleNodesA; scaleNodesA.scaleNodes( 1.3,1)","Shift+.")
nodegraphMenu.addCommand("scaleNodesContract", "import scaleNodesA; scaleNodesA.scaleNodes( .7, 1 )","Ctrl+Shift+.")






nuke.tprint("_"*100);nuke.tprint("my user is loaded");nuke.tprint("_"*100)


