import nuke
import nukescripts
from nukescripts import snap3d
def cardMy():
    nuke.createNode("Card2")
        
        
        
        
def cardMybkp():
    a = nukescripts.snap3d.getSelection()
    if a.length==1:
        n = nuke.createNode("Card2")
        nukescripts.snap3d.translateToPoints(n)
    elif a.length==2:
        n = nuke.createNode("Card2")
        nukescripts.snap3d.translateRotateToPoints(n)
    elif a.length>2:
        n = nuke.createNode("Card2")
        nukescripts.snap3d.translateRotateScaleToPoints(n)
    else:
        nuke.createNode("Card2")
