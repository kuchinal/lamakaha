import nuke
def MergeSplit():
    t = nuke.selectedNode()
    depB = t.dependencies(nuke.INPUTS)[0]
    try:
        depA = t.dependencies(nuke.INPUTS)[1]
    except:
        depA = t.dependencies(nuke.INPUTS)[0]
    x2 = depA['xpos'].value()
    y2 = depA['ypos'].value()
    x2 = int(x2)
    y2 = int(y2)
    x1 = t['xpos'].value()
    y1 = t['ypos'].value()
    x1 = int(x1)
    y1 = int(y1)
    dot = nuke.nodes.Dot()
    dot.setXYpos(x1-100,y1+5)
    dot2 = nuke.nodes.Dot()
    dot2.setXYpos(x1-100,y2+5)
    dot2.setInput(0,depA)
    dot.setInput(0,dot2)
    t.setInput(1,dot)
