Tuesday, October 15, 2013
(17:20) martin: harhar
Friday, October 25, 2013
(11:39) Alexey: Z:/_projects/Die_Bergretter_5/files/nuke/F02/Mattepainting/

(13:14) martin: spark also translated. 
(13:14) martin: magnificent. 
(13:15) martin: shot f03_035 updated with less defocused BG
(13:18) martin: shot f03_075 rerendered, just to be sure everything is the same version
Tuesday, October 29, 2013
(09:48) martin: hello
(09:48) martin: message
(11:42) martin: the MP was approved, and it had some fog/haze in it, so we probably can do that
(11:42) martin: we'll also get 5 frames in 4k
(11:52) Alexey: cool
Wednesday, October 30, 2013
(18:52) Alexey: \\10.0.43.5\BlackBunker\_projects\Die_Bergretter_5\paint\F02_topView\Neuer Ordner
(18:55) martin: thanks
(18:58) Alexey: np
Wednesday, November 6, 2013
(14:23) martin: set cut_paste_input [stack 0]
version 7.0 v9
push $cut_paste_input
NoOp {
name NoOp22
selected true
xpos -983
ypos 2164
}
set N28490730 [stack 0]
push $N28490730
Grain2 {
name Grain2_2
label "Kodak 5248"
selected true
xpos -919
ypos 2242
red_size 3
green_size 1.1
blue_size 5.4
red_i 0.215
green_i 0.215
blue_i 0.21
red_m 0.125
green_m 0.035
blue_m 0.1
black {0 0 0}
minimum {0.01 0 0}
maskgrain false
}
Dissolve {
inputs 2
which 0.5
name Dissolve3
selected true
xpos -983
ypos 2321
}

 
(09:58) martin: *************** world_to_XYZ********************
 
import math
import nuke
 
def bakeCamera():
    ver=str(nuke.NUKE_VERSION_MAJOR)+str(nuke.NUKE_VERSION_MINOR)
    if int(ver) < 61:
        nuke.message("This script works only withe Nuke 6.1 and higher")
        return
 
    if len(nuke.selectedNodes()) != 1:
        nuke.message("Select Camera Node")
        return
 
    n=nuke.selectedNode()
    if n.Class() != "Camera2":
        nuke.message("No Camera selected")
        return
 
    firstFrame = int(nuke.numvalue('root.first_frame'))
    lastFrame = int(nuke.numvalue('root.last_frame'))
    step = 1
    _range = str(nuke.FrameRange(firstFrame,lastFrame,step))
    r = nuke.getInput('Enter Frame Range:', _range)
 
    bakeFocal = False
    bakeHaperture = False
    bakeVaperture = False
 
 
    k = n['world_matrix']
 
    newCam = nuke.createNode("Camera2")
    newCam.setInput(0, None)
    newCam['rotate'].setAnimated()
    newCam['translate'].setAnimated()
 
    oldFocal = n['focal']
    if oldFocal.isAnimated() and not (oldFocal.animation(0).constant()):
        newCam['focal'].setAnimated()
        bakeFocal = True
    else:
        newCam['focal'].setValue(oldFocal.value())
 
    oldHaperture = n['haperture']
    if oldHaperture.isAnimated() and not (oldHaperture.animation(0).constant()):
        newCam['haperture'].setAnimated()
        bakeHaperture = True
    else:
        newCam['haperture'].setValue(oldHaperture.value())
 
    oldVaperture = n['vaperture']
    if oldVaperture.isAnimated() and not (oldVaperture.animation(0).constant()):
        newCam['vaperture'].setAnimated()
        bakeVaperture = True
    else:
        newCam['vaperture'].setValue(oldVaperture.value())
 
    newCam['win_translate'].setValue(n['win_translate'].value())
    newCam['win_scale'].setValue(n['win_scale'].value())
 
    for x in nuke.FrameRange(r):
        m = nuke.math.Matrix4()
        for y in range(k.height()):
            for z in range(k.width()):
                m[z+(y*k.width())] = k.getValueAt(x, (y+(z*k.width())))
 
        rotM = nuke.math.Matrix4(m)
        rotM.rotationOnly() 
        rot = rotM.rotationsZXY()
 
        newCam['rotate'].setValueAt(math.degrees(rot[0]), x, 0)
        newCam['rotate'].setValueAt(math.degrees(rot[1]), x, 1)
        newCam['rotate'].setValueAt(math.degrees(rot[2]), x, 2)
        newCam['translate'].setValueAt(k.getValueAt(x, 3), x, 0)
        newCam['translate'].setValueAt(k.getValueAt(x, 7), x, 1)
        newCam['translate'].setValueAt(k.getValueAt(x, 11), x, 2)
 
        if bakeFocal:
            newCam['focal'].setValueAt(oldFocal.getValueAt(x), x)
        if bakeHaperture:
            newCam['haperture'].setValueAt(oldHaperture.getValueAt(x), x)
        if bakeVaperture:
            newCam['vaperture'].setValueAt(oldVaperture.getValueAt(x), x)