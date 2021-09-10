import nuke
import nukescripts
import os
#


#######
UserDir = os.path.dirname(__file__)

n11,n10 = False,True
if nuke.NUKE_VERSION_MAJOR > 10:
    n11 = True;n10 = False

    


nuke.tprint("_"*100);nuke.tprint("now loading my user");nuke.tprint("_"*100);nuke.tprint("_"*100)


import knob_scripter
import mps3





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
import AnimationMaker
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
nodesMenu.addCommand("3D/ReflectionMy", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/reflectionMy.nk')",icon="my.png") 
nodesMenu.addCommand('3D/WorldToRTS - calculate world matrix to TRS','import WorldToRTS; WorldToRTS.consolidateAnimatedNodeTransforms()',icon="Camera.png")
nodesMenu.addCommand("3D/Camera", "nuke.createNode(\"Camera2\")","F11",  icon="Camera.png")
nodesMenu.addCommand("3D/ScanlineRender", "import slrcreate; slrcreate.slrcreate()","F12",icon = "Render.png")
nodesMenu.addCommand("3D/Card", "nuke.createNode(\"Card2\")","F10",  icon="Card.png")
nodesMenu.addCommand("3D/Cube", "nuke.createNode(\"Cube\")","Ctrl+F10",  icon="Cube.png")
nodesMenu.addCommand("3D/Sphere", "nuke.createNode(\"Sphere\")","Alt+F10",  icon="Card.png")


nodesMenu.addCommand("3D/CameraTracker", "nuke.createNode(\"CameraTracker1_0\")", "alt+F12",icon="Tracker.png")
nodesMenu.addCommand("3D/Project3D", "nuke.createNode(\"Project3D\")","Ctrl+F11", icon="Shader_cam.png")
nodesMenu.addCommand("3D/Light", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/LightTargeted.nk')","+l", icon="PointLight.png")

nodesMenu.addCommand("Draw/PerspectiveGuide", "nuke.createNode('BB_PerspectiveGuide_1_1_0')", icon="BB_icon.png")
nodesMenu.addCommand("Draw/UV generator", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/UVgenerator.nk')",icon="UVv.png")
nodesMenu.addCommand("Draw/Caustic", "nuke.createNode(\'Caustics\')") 
nodesMenu.addCommand('Draw/Grid', "nuke.createNode(\"Grid\")","Ctrl+F3",icon = "Grid.png")
nodesMenu.addCommand("Draw/Noise", "nuke.createNode(\"Noise\")","Ctrl+F2", icon="Noise.png")
nodesMenu.addCommand("Draw/Constant white", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ConstantWhite.nk')","Ctrl+f1", icon="Constant.png")
nodesMenu.addCommand("Draw/RotoPaint", "nuke.createNode(\"RotoPaint\")","Alt+f2")

nodesMenu.addCommand("Merge/ContactSheetMy", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ContactSheetMy.nk')")
nodesMenu.addCommand("Merge/Difference", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Difference.nk')", icon="my.png")  
nodesMenu.addCommand('Merge/Operations/Over', 'import Operations; Operations.over()',"ctrl+alt+o")
nodesMenu.addCommand('Merge/Operations/Plus', 'import Operations; Operations.plus()',"ctrl+alt+p")
nodesMenu.addCommand('Merge/Operations/Copy', 'import Operations; Operations.ccopy()',"ctrl+alt+k")
nodesMenu.addCommand('Merge/Operations/Minus', 'import Operations; Operations.minus()',"ctrl+alt+Shift+p")
nodesMenu.addCommand('Merge/Operations/Under', 'import Operations; Operations.under()',"ctrl+alt+Shift+o")
nodesMenu.addCommand('Merge/Operations/Divide', 'import Operations; Operations.divide()',"ctrl+alt+d")
nodesMenu.addCommand('Merge/Operations/Disjoint-over', 'import Operations; Operations.disjoint()',"ctrl+alt+Shift+d")
nodesMenu.addCommand('Merge/Operations/Multiply', 'import Operations; Operations.multiply()',"ctrl+alt+m")
nodesMenu.addCommand('Merge/Operations/From', 'import Operations; Operations.fromm()',"ctrl+alt+f")
nodesMenu.addCommand('Merge/Operations/In', 'import Operations; Operations.inn()',"ctrl+alt+i")
nodesMenu.addCommand('Merge/Operations/Out', 'import Operations; Operations.out()',"ctrl+alt+shift+i")
nodesMenu.addCommand('Merge/Operations/Screen', 'import Operations; Operations.screen()',"ctrl+alt+s")
nodesMenu.addCommand('Merge/Operations/Max', 'import Operations; Operations.xor()',"ctrl+alt+x")
nodesMenu.addCommand('Merge/Operations/Min', 'import Operations; Operations.xorm()',"ctrl+alt+Shift+x")
nodesMenu.addCommand('Merge/Operations/Atop', 'import Operations; Operations.atop()',"ctrl+alt+a")
nodesMenu.addCommand('Merge/Operations/average', 'import Operations; Operations.aver()',"ctrl+alt+Shift+a")

nodesMenu.addCommand('IO/Preferences override','import preferencesOverride; preferencesOverride.preferencesOverride()')
nodesMenu.addCommand("IO/Start Trmplate", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/StartTemplate.nk')")
nodesMenu.addCommand("IO/Review", "import review; review.review()","F9", icon="my.png")
nodesMenu.addCommand('IO/ExplorerJPEG', 'import Explorer; Explorer.ExplorerJPEG()',"Shift+Alt+r",icon = "Explorer.png")


nodesMenu.addCommand("Filter/Channel Blur","nuke.createNode(\'ChannelBlur\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/Lens Kernel","nuke.createNode(\'LensKernel\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/Filler","nuke.createNode(\'Filler\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/VoronoiGradient","nuke.createNode(\'VoronoiGradient\')",icon = "Ramp.png")
nodesMenu.addCommand("Filter/ErodeMini", "nuke.createNode(\'ErodeMini\')", "e", icon="Erode.png")
nodesMenu.addCommand("Filter/Exponential Glow My", "nuke.createNode(\'Eglow\')","Shift+g",icon="Glow.png")
nodesMenu.addCommand("Filter/DarkWrap","nuke.createNode(\'DarkWrap\')",icon = "Blur.png")
nodesMenu.addCommand("Filter/VolumeRays", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/VolumeRays.nk')", icon="Ramp.png")
nodesMenu.addCommand("Filter/ChromAbb",  "nuke.nodePaste(UserDir+'/Folders/NukeScripts/ChromAbb.nk')", icon="FlareFactoryPlus.png")
nodesMenu.addCommand("Filter/PolarCoordinates", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/PolarCoordinates.nk')",icon="my.png")
nodesMenu.addCommand("Sharpen", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Sharpen.nk')")

nodesMenu.addCommand('Transform/CardToTrack', "nuke.createNode(\"CardToTrack\")",icon = "Card.png")
nodesMenu.addCommand('Transform/TrackToRoto','import TrackToRoto; TrackToRoto.RotoFromTrack()',"p",icon="Tracker.png")
nodesMenu.addCommand('Transform/concatenate2Dtransforms','importconcatenate2Dtransforms; concatenate2Dtransforms.transformstoMatrix()',icon="Tracker.png")
nodesMenu.addCommand('Transform/Smoother','import  Smoother; Smoother.Smoother()') 
nodesMenu.addCommand("Transform/Offset", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/Offset.nk')", icon="my.png")
nodesMenu.addCommand("Transform/ITransform","nuke.nodePaste(UserDir+'/Folders/NukeScripts/iTransform.nk')","Alt+f3", icon="my.png")
nodesMenu.addCommand("Transform/TransformMasked", "nuke.createNode(\"TransformMasked\")","Alt+f6", icon="TransformMasked.png")
nodesMenu.addCommand("Transform/Cr", "import cropMy;cropMy.cropMy()","F6", icon="Crop.png")
nodesMenu.addCommand("Transform/CornerPin", "nuke.createNode(\"CornerPinMy11\")", "shift+ctrl+c", icon="CornerPin.png")
nodesMenu.addCommand('Reformat','import myReformat; myReformat.myReformat()',"ctrl+r", icon="Reformat.png")
nodesMenu.addCommand("ReformatCrop","import ReformatCrop; ReformatCrop.ReformatCrop()",'ctrl+shift+r')
nodesMenu.addCommand("Tracker", "nuke.createNode(\"Tracker4\")", "ctrl+t",icon="Tracker.png")


nodesMenu.addCommand('Nodegraph/Auto Backdrop', 'import autoBackdropp; autoBackdropp.autoBackdrop()', 'alt+b',icon = "Backdrop.png")
nodesMenu.addCommand('Nodegraph/Auto Sticky', 'import autoSticky; autoSticky.autoSticky()', 'alt+n',icon = "Backdrop.png")
nodesMenu.addCommand("Nodegraph/Copy file names", "import copyFileName; copyFileName.copyFileName()","Ctrl+Alt+Shift+c",icon="ColorWheel.png")
nodesMenu.addCommand('Nodegraph/Open Read in File Browser', 'import Explorer; Explorer.ExplorerJPEG()',"Alt+Shift+r",icon = "Explorer.png")
nodesMenu.addCommand('Nodegraph/HiddenPostages Toggle visibility','stamps.anchorSelectWireds()', "z",icon = "PostageStamp.png")
nodesMenu.addCommand('Nodegraph/W_scaleTree', 'import W_scaleTree; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
nodesMenu.addCommand("Nodegraph/Create inverted axis from curent axis ", "import inverter; inverter.inverter()",icon = "Axis.png")
nodesMenu.addCommand('Nodegraph/@;Label', 'import Label; Label.Label()',"n",icon = "Label.png")
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
nodesMenu.addCommand('Nodegraph/autoplace nodes', '[n.autoplace() for n in nuke.selectedNodes()]',"Ctrl+Alt+l")


nodesMenu.addCommand("Color/Full Fade", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/FullFade.nk')","Shift+f",icon="my.png")       
nodesMenu.addCommand("Color/Expression", "import expressionMy; expressionMy.expressionMy()","Alt+f1", icon="my.png")
nodesMenu.addCommand("Color/shuffle/shuffleRed",'import shuffle_Smart;shuffle_Smart.shuffleRed()',"r")
nodesMenu.addCommand("Color/shuffle/shuffleAlpha",'import shuffle_Smart;shuffle_Smart.shuffleAlpha()',"a")
nodesMenu.addCommand("Color/shuffle/shuffleBlue",'import shuffle_Smart;shuffle_Smart.shuffleBlue()',"b")
nodesMenu.addCommand("Color/shuffle/shuffleGreen",'import shuffle_Smart;shuffle_Smart.shuffleGreen()',"g")
nodesMenu.addCommand("Color/shuffleCreate",'import shuffle_Smart;shuffle_Smart.shuffleCreate()',"s")
nodesMenu.addCommand("Color/shuffleDepth",'import shuffle_Smart;shuffle_Smart.shuffleDepth()',"d")
nodesMenu.addCommand('Color/Invert', "nuke.createNode(\"Invert\")","i",icon="my.png")       
nodesMenu.addCommand("Color/Multiply", "import fademult;fademult.fademult()","f", icon="ColorMath.png")
nodesMenu.addCommand("Color/HueCorrect", "nuke.createNode(\"HueCorrect\")","h", icon="HueCorrect.png")
nodesMenu.addCommand("Color/ColorLookup", "nuke.createNode(\"ColorLookup\")","Ctrl+F4",icon="ColorLookup.png")
nodesMenu.addCommand("Color/Clamp", "nuke.createNode(\"Clamp\")","F4", icon="Clamp.png")
nodesMenu.addCommand("Color/Unpremult", "nuke.createNode(\"Unpremult\")","u", icon="Unpremult.png")
nodesMenu.addCommand("Color/Premult", "nuke.createNode(\"Premult\")","ctrl+u", icon="Premult.png")
nodesMenu.addCommand("Color/CheckerBoard", "nuke.createNode(\"CheckerBoard2\")","f2", icon="CheckerBoard.png")
nodesMenu.addCommand("Color/Saturation", "nuke.createNode('Saturation')","Alt+F9")
nodesMenu.addCommand("Color/HueShift", "nuke.createNode(\"HueShift\")","Ctrl+h", icon="HueShift.png")
nodesMenu.addCommand("Color/HSVTool", "nuke.createNode(\"HSVTool\")","Shift+h", icon="HSVTool.png")

nodesMenu.addCommand('Keyer/IBKMy', 'nuke.nodePaste(UserDir+"/Folders/NukeScripts/IBK.nk")',"Ctrl+F5",icon="luma.png")
nodesMenu.addCommand("Keyer/AddKeyer", "nuke.createNode('AddKeyer')", icon="luma.png")
nodesMenu.addCommand("Keyer/LumaKey", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/LumaKey.nk')","Ctrl+F7",icon="luma.png")

nodesMenu.addCommand('Keyer/Edge/EdgeScatter', "nuke.createNode(\"EdgeScatter\")",icon = "Defocus.png")
nodesMenu.addCommand("Keyer/Despill/DespillMadness", "nuke.createNode('DespillMadnessMy')", icon="HueKeyer.png")
nodesMenu.addCommand("Keyer/Edge/EdgeScatter", "nuke.createNode('EdgeScatter')", icon="Difference.png")
nodesMenu.addCommand("Keyer/Edge/VectorExtendEdge", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/VectorExtendEdge.nk')","v",icon="Difference.png")
nodesMenu.addCommand("Keyer/Edge/UVExtendEdge", "nuke.nodePaste(UserDir+'/Folders/NukeScripts/edgeExtendMatrix.nk')",icon="Difference.png")
nodesMenu.addCommand("Keyer/Edge/RoughEdge", "nuke.createNode(\'RoughEdgeMy\')")
nodesMenu.addCommand("Keyer/Edge/Erode_My", "nuke.createNode(\"Erode_My\")","Ctrl+Shift+e",icon="ErodeBlur.png")

nodesMenu.addCommand('Other/NameMy','import NameMy; NameMy.NameMy()',"Ctrl+Shift+n")
nodesMenu.addCommand('Other/NodeInfo','import Info; Info.Info()',"Ctrl+i")
nodesMenu.addCommand("Other/&Project Settings...", "nuke.showSettings()","*")


nodesMenu.addCommand('Time/FrameHoldMy', 'FrameHoldMy.FrameHoldMy()',"F5",icon = "pause.png")
nodesMenu.addCommand("Time/Retime", "nuke.createNode(\"Retime\")","Alt+Ctrl+r")
nodesMenu.addCommand("Time/Shortcuted/Timewarp", "nuke.createNode(\"TimeWarp\")","Alt+Ctrl+t")
nodesMenu.addCommand("Time/Shortcuted/Go to frame", "nukescripts.goto_frame()","Alt+g", icon="my.png")

nodesMenu.addCommand('Channel/BlackAlpha', 'import Black; Black.Black()', "Ctrl+b")
nodesMenu.addCommand('Channel/WhiteAlpha', 'import Black; Black.White()', "Ctrl+Shift+b")
nodesMenu.addCommand("Channel/Remove", "nuke.createNode(\"Remove\")", "Ctrl+Alt+Shift+b", icon="Remove.png")



#######################################    NODEGRAPH MENU    ####################################################
nodegraphMenu = nuke.menu('Node Graph')
nodegraphMenu.addCommand('@;Dots ', 'import Dots; Dots.Dots()', ',',icon = "Dot.png")
nodegraphMenu.addCommand('@;Transform', 'import myTransform; myTransform.transformThis()', 't')
nodegraphMenu.addCommand('@;Merge', 'import myMerge; myMerge.mergeThis()', 'm',shortcutContext=2)
nodegraphMenu.addCommand("@;MyCC", "import myCC; myCC.myCC()","c")








nuke.tprint("_"*100);nuke.tprint("my user is loaded");nuke.tprint("_"*100)





# def example():
#     import sys
#     from PySide2 import QtCore, QtGui, QtWidgets
    
#     pixmap = QtGui.QPixmap('/mnt/Hobby/projects/toe/07_Masters/toe.png')
#     label = QtWidgets.QLabel()
#     label.setPixmap(pixmap)
#     label.setScaledContents(1)
#     label.resize(1146/2, 1468/2)
#     #label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#     label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#     label.show()
# nuke.addOnCreate(lambda: example() , nodeClass="Toe2")



def example():
    nuke.thisNode()["icon"].setValue('/mnt/Hobby/projects/toe/07_Masters/toeST.png')

nuke.addOnCreate(lambda: example() , nodeClass="Toe2")


































