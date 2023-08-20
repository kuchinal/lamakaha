

# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
#
# This example will automatically put a backdrop behind the selected nodes
#

import nuke, operator, random

def autoBackdroppp():
    import random
    selNodes = nuke.selectedNodes()
    if not selNodes:
        return nuke.nodes.BackdropNode()
    
    # find min and max of positions
    positions = [(i.xpos(), i.ypos()) for i in selNodes]
    xPos = sorted(positions, key = operator.itemgetter(0))
    yPos = sorted(positions, key = operator.itemgetter(1))
    xMinMaxPos = (xPos[0][0], xPos[-1:][0][0])
    yMinMaxPos = (yPos[0][1], yPos[-1:][0][1])
    
    n = nuke.nodes.BackdropNode(xpos = xMinMaxPos[0]-10,
                                bdwidth = xMinMaxPos[1]-xMinMaxPos[0]+110,
                                ypos = yMinMaxPos[0]-85,
                                bdheight = yMinMaxPos[1]-yMinMaxPos[0]+160,
                                tile_color = int((random.random()*(13-11)))+11,
                                note_font_size = 60, note_font = 1)
    
    
    
    r = (float(random.randint( 20, 40)))/100
    g = (float(random.randint( 10, 50)))/100
    b = (float(random.randint( 15, 60)))/100
    t = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
    
    
    panel=nuke.Panel("Postage Name")
    panel.addSingleLineInput("Label","")
    panel.addEnumerationPulldown("Color", "General Precomp Red Green Blue Magenta Cyan Yellow")
    panel.addSingleLineInput("Font",30)
    panel.addBooleanCheckBox('bookmark', False)
    
    
    panel.show()
    color = panel.value('Color')
    text = panel.value('Label')
    bookmark = panel.value('bookmark')
    font = int(panel.value('Font'))
    label = n['label'].setValue(text)
    
    n['note_font_size'].setValue(font)
    n['bookmark'].setValue(0)
    if  color == "General":
        icon = text
        n['tile_color'].setValue(t)
        n['label'].setValue(icon)
    
    if  bookmark == 1:
        n['bookmark'].setValue(1)
    
    if  color == "Precomp":
        n['tile_color'].setValue(2466250752L)
        n['label'].setValue("Precomp")
        m = nuke.PyScript_Knob("onrenderfarm","<font color='Black'><b>on renderfarm","nuke.thisNode()['tile_color'].setValue(255)")
        n.addKnob(m) 
        m = nuke.PyScript_Knob("prerendered","<font color='Red'><b>prerendered","nuke.thisNode()['tile_color'].setValue(2466250752L)")
        n.addKnob(m) 
        m = nuke.PyScript_Knob("needprerender","<font color='White'><b>need prerender","nuke.thisNode()['tile_color'].setValue(4294967295)")
        n.addKnob(m) 
        w = nuke.selectedNode()
        x = w['xpos'].value()
        y = nuke.selectedNode()['ypos'].value()
        dep = w.dependencies()[0]
        dotA = nuke.createNode("Dot")
        dotA.setXYpos(x+150,y+10)
        dotA.setInput(0,dep)
        w.setInput(0,dotA)
        n['bdwidth'].setValue(200)
        n['bdheight'].setValue(250)
    if  color == "Red":
        icon = text
        n['tile_color'].setValue(2466250752L)
        n['label'].setValue(icon)
    if   color == "Green":
        icon = text
        n['tile_color'].setValue(1063467008L)
        n['label'].setValue(icon)
    if   color == "Blue":
        icon = text
        n['tile_color'].setValue(1027575296L)
        n['label'].setValue(icon)
    if   color == "Magenta":
        icon =text
        n['tile_color'].setValue(1358974720L)
        n['label'].setValue(icon)
    if   color== "Cyan":
        icon = text
        n['tile_color'].setValue(861493759)
        n['label'].setValue(icon)
    if   color== "Yellow":
        icon = text
        n['tile_color'].setValue(2526413055)
        n['label'].setValue(icon)
    n['selected'].setValue(False)
    # revert to previous selection
    [i['selected'].setValue(True) for i in selNodes]
    
    return n
autoBackdroppp()

