import nuke
import nukescripts

def Split():
    left = nuke.selectedNode()



    x=left['xpos'].value()
    y = left['ypos'].value()

    right = nukescripts.edit.node_copypaste()
    right = nuke.selectedNode()

    z = left['file'].value()
    t = z.replace("%V","left")
    z = left['file'].setValue(t)

    l = right['file'].value()
    t = l.replace("%V","right")
    l = right['file'].setValue(t)

    right.setXYpos(x+150,y)
    right['selected'].setValue(False)
    split = nuke.nodes.JoinViews()
    split.setInput(0,left)
    split.setInput(1,right)
    split.setXYpos(x+70,y+150)
    split['selected'].setValue(False)
    left['selected'].setValue(False)

