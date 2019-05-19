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
animatedSnap3D.menuEntry()


#######################################    KNOB DEFAULTS    ####################################################
import knobDefaults 
knobDefaults.knobDefaults()

#######################################    ON CREATE FUNCTIONS    ####################################################
import onCreateFunctions
onCreateFunctions.onCreateFunctions()




#######################################    VIEWER MENU    ####################################################
viewerMenu = nuke.menu('Viewer')
viewerMenu.addCommand("saveImage", "import saveImage; saveImage.saveImage()")

#######################################    ANIMATION MENU    ####################################################
animationMenu = nuke.menu('Animation')
animationMenu.addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')





#######################################    MAIN MENU    ####################################################odesMenu = nuke.menu( 'Nodes' )
nodesMenu = nuke.menu('Nodes')
nodesMenu.addCommand("AOVs/Fresnel ", "nuke.createNode(\'Fresnel\')", icon="Wireframe.png")
nodesMenu.addCommand("AOVs/Relight/Relight_N", "nuke.createNode('Relight_N')", icon="my.png")
nodesMenu.addCommand("AOVs/Pref_Sticker", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Pref_Sticker.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Mask_3D", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Mask_3D.nk')","Ctrl+F12",icon="my.png") 
nodesMenu.addCommand("AOVs/Lambert_Shader_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Lambert_Shader_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Mask3DCubical_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Mask3DCubical_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Mask3DGradient_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Mask3DGradient_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Mask3DSpherical_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Mask3DSpherical_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Texture_Generator_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Texture_Generator_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/Texture_Projection_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_Texture_Projection_ik.nk')", icon="my.png")
nodesMenu.addCommand("AOVs/TransformWorld_ik", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/WorldPos_TransformWorld_ik.nk')", icon="my.png")


nodesMenu.addCommand("3D/MotionBlurCurved ", "nuke.createNode(\'MotionBlurCurved\')",icon ="MotionBlur2D.png")
nodesMenu.addCommand("3D/ReflectionMy", "nuke.nodePaste(UserDir+'/GeneralSetups/reflectionMy.nk')",icon="my.png") 
nodesMenu.addCommand('3D/WorldToRTS - calculate world matrix to TRS','WorldToRTS.consolidateAnimatedNodeTransforms()',icon="Camera.png")


nodesMenu.addCommand("Other/PerspectiveGuide", "nuke.createNode('BB_PerspectiveGuide_1_1_0')", icon="BB_icon.png")

nodesMenu.addCommand("Draw/UV generator", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/UVgenerator.nk')",icon="UVv.png")
nodesMenu.addCommand("Draw/Caustic", "nuke.createNode(\'Caustics\')") 

nodesMenu.addCommand("Merge/ContactSheetMy", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ContactSheetMy.nk')")
nodesMenu.addCommand("Merge/Difference", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Difference.nk')", icon="my.png")  

nodesMenu.addCommand('IO/Preferences override','import preferencesOverride; preferencesOverride.preferencesOverride()')
nodesMenu.addCommand("IO/Start Trmplate", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/StartTemplate.nk')")
nodesMenu.addCommand("IO/Review", "import review; review.review()","F9", icon="my.png")

nodesMenu.addCommand("Filter/Channel Blur","nuke.createNode(\'ChannelBlur\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/Lens Kernel","nuke.createNode(\'LensKernel\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/Filler","nuke.createNode(\'Filler\')",icon = "Blur.png")
nodesMenu.addCommand('Filter/EdgeScatter', "nuke.createNode(\"EdgeScatter\")",icon = "Defocus.png")
nodesMenu.addCommand("Filter/VoronoiGradient","nuke.createNode(\'VoronoiGradient\')",icon = "Ramp.png")
nodesMenu.addCommand("Filter/ErodeMini", "nuke.createNode(\'ErodeMini\')", "e", icon="Erode.png")
nodesMenu.addCommand("Filter/Exponential Glow My", "nuke.createNode(\'Eglow\')","Shift+g",icon="Glow.png")
nodesMenu.addCommand("Filter/Rough Edge-", "nuke.createNode(\'RoughEdgeMy\')")
nodesMenu.addCommand("Filter/DarkWrap","nuke.createNode(\'DarkWrap\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/VolumeRays", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/VolumeRays.nk')", icon="Ramp.png")
nodesMenu.addCommand("Filter/ChromAbb",  "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ChromAbb.nk')", icon="FlareFactoryPlus.png")
nodesMenu.addCommand("Filter/PolarCoordinates", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/PolarCoordinates.nk')",icon="my.png")

nodesMenu.addCommand('Transform/CardToTrack', "nuke.createNode(\"CardToTrack\")",icon = "Card.png")
nodesMenu.addCommand('Transform/TrackToRoto','import TrackToRoto; TrackToRoto.RotoFromTrack()',"Shift+p",icon="Tracker.png")
nodesMenu.addCommand('Transform/concatenate2Dtransforms','importconcatenate2Dtransforms; concatenate2Dtransforms.transformstoMatrix()',icon="Tracker.png")
nodesMenu.addCommand('Transform/Smoother','import  Smoother; Smoother.Smoother()') 
nodesMenu.addCommand("Transform/Offset", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Offset.nk')", icon="my.png")
nodesMenu.addCommand("Transform/ITransform","nuke.nodePaste(UserDir+'/Folders/NukeScripts/iTransform.nk')","Alt+f3", icon="my.png")

nodesMenu.addCommand('Nodegraph/Auto Backdrop', 'import autoBackdropp; autoBackdropp.autoBackdrop()', 'alt+b',icon = "Backdrop.png")
nodesMenu.addCommand('Nodegraph/Auto Sticky', 'import autoSticky; autoSticky.autoSticky()', 'alt+n',icon = "Backdrop.png")
nodesMenu.addCommand("Nodegraph/Copy file names", "import copyFileName; copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")
nodesMenu.addCommand('Nodegraph/Open Read in File Browser', 'import Explorer; Explorer.ExplorerJPEG()',"Alt+Shift+r",icon = "Explorer.png")
nodesMenu.addCommand('Nodegraph/HiddenPostages Toggle visibility','stamps.anchorSelectWireds()', "z",icon = "PostageStamp.png")
nodesMenu.addCommand('Nodegraph/W_scaleTree', 'import W_scaleTree; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
nodesMenu.addCommand("Nodegraph/Create inverted axis from curent axis ", "import inverter; inverter.inverter()",icon = "Axis.png")
nodesMenu.addCommand('Nodegraph/@;Label', 'Label.Label()',"n",icon = "Label.png")
nodesMenu.addCommand('Nodegraph/Paste To Selected', 'pasteToSelected.pasteToSelected()',"Alt+f5", index=10,icon="my.png")
nodesMenu.addCommand('Nodegraph/Stamp', 'stamps.goStamp()', "F8",icon = "PostageStamp.png")
nodesMenu.addCommand("Nodegraph/Find Pigs", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/findPigs.nk')")
nodesMenu.addCommand('Nodegraph/Align/vertically', 'import alignNodes; alignNodes.alignNodes( nuke.selectedNodes(), direction="x" )',"Ctrl+l")
nodesMenu.addCommand("Nodegraph/Backdrops/Fix Layering", "import backdropTools; backdropTools.fixBackdropDepth()")
nodesMenu.addCommand('Nodegraph/Paste To Selected', 'import pasteToSelected; pasteToSelected.pasteToSelected()',"Alt+f5", index=10,icon="my.png")
nodesMenu.addCommand('Nodegraph/getColor','import getColor; getColor.getColor()',icon="my.png")
nodesMenu.addCommand("Nodegraph/Splay First", "nuke.splayNodes(False, False)", "Down")
nodesMenu.addCommand("Nodegraph/Connect", "nuke.connectNodes(False, False)", "Up")
nodesMenu.addCommand('Nodegraph/Align/horizontally', 'import alignNodes; alignNodes.alignNodes( nuke.selectedNodes(), direction="y" )',"l")
nodesMenu.addCommand("Nodegraph/scaleNodesExpand", "import scaleNodesA; scaleNodesA.scaleNodes( 1.3,1)","Shift+.")
nodesMenu.addCommand("Nodegraph/scaleNodesContract", "import scaleNodesA; scaleNodesA.scaleNodes( .7, 1 )","Ctrl+Shift+.")

nodesMenu.addCommand("Color/Full Fade", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/FullFade.nk')","Shift+f",icon="my.png")       
nodesMenu.addCommand("Color/Expression", "import expressionMy; expressionMy.expressionMy()","Alt+f1", icon="my.png")
nodesMenu.addCommand("Color/shuffle/shuffleRed",'import shuffle_Smart;shuffle_Smart.shuffleRed()',"r")
nodesMenu.addCommand("Color/shuffle/shuffleAlpha",'import shuffle_Smart;shuffle_Smart.shuffleAlpha()',"a")
nodesMenu.addCommand("Color/shuffle/shuffleBlue",'import shuffle_Smart;shuffle_Smart.shuffleBlue()',"b")
nodesMenu.addCommand("Color/shuffle/shuffleGreen",'import shuffle_Smart;shuffle_Smart.shuffleGreen()',"g")
nodesMenu.addCommand("Color/shuffleCreate",'import shuffle_Smart;shuffle_Smart.shuffleCreate()',"s")
nodesMenu.addCommand("Color/shuffleDepth",'import shuffle_Smart;shuffle_Smart.shuffleDepth()',"d")
nodesMenu.addCommand('Color/Invert', "nuke.createNode(\"Invert\")","i",icon="my.png")       
nodesMenu.addCommand("Color/Multiply", "fademult;fademult.fademult()","f", icon="ColorMath.png")
nodesMenu.addCommand("Color/HueCorrect", "nuke.createNode(\"HueCorrect\")","h", icon="HueCorrect.png")

#######################################    NODEGRAPH MENU    ####################################################
nodegraphMenu = nuke.menu('Node Graph')
nodegraphMenu.addCommand('My/Dots ', 'Dots.Dots()', ',',icon = "Dot.png")
nodegraphMenu.addCommand('My/Transform', 'myTransform.transformThis()', 't')
nodegraphMenu.addCommand('My/Merge', 'myMerge.mergeThis()', 'm',shortcutContext=2)
nodegraphMenu.addCommand("My/MyCC", "myCC.myCC()","c")
#nodegraphMenu.addCommand('Align/autoplace', 'autoplace()',"Ctrl+Alt+l")





nuke.tprint("_"*100);nuke.tprint("my user is loaded");nuke.tprint("_"*100)










































