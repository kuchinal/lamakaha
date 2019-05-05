

# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
#
# This example will automatically put a backdrop behind the selected nodes
#

import nuke, operator, random

def autoBackdrop():
    import random
    selNodes = nuke.selectedNodes()
    if not selNodes:
        s = nuke.createNode("Blur")
        s.setSelected(True)
        nuke.delete(s)
        return nuke.createNode('BackdropNode')

        
    
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
    
    Bn = n
    r = (float(random.randint( 20, 40)))/100
    g = (float(random.randint( 10, 50)))/100
    b = (float(random.randint( 15, 60)))/100
    t = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
    
    
    panel=nuke.Panel("Postage Name")
    panel.addSingleLineInput("Label","")
    #panel.addSingleLineInput("Font",100)
    panel.addEnumerationPulldown("Font", " big middle small tiny huge")
    panel.addEnumerationPulldown("Color", "Random Red Green Blue Magenta Cyan Yellow")
    panel.addEnumerationPulldown('Description','sticky normal')
    panel.addBooleanCheckBox('Bold', True)
    panel.addBooleanCheckBox('bookmark', False)

    panel.show()
    color = panel.value('Color')
    text = panel.value('Label')
    bookmark = panel.value('bookmark')
    fontA = panel.value('Font')
    fonts = {'big':100, 'huge':300, 'middle':50, 'small':20, 'tiny':10}
    fontsX = {'big':10, 'huge':10, 'middle':10, 'small':10, 'tiny':10}
    fontsY = {'big':210, 'huge':315, 'middle':155, 'small':123, 'tiny':113}
    font = fonts[fontA]
    fontsX = fontsX[fontA]
    fontsY = fontsY[fontA]
    bold = panel.value('Bold')
    sticky = panel.value('Description')
    n['note_font_size'].setValue(font)
    n['bookmark'].setValue(0)
    if bold == True:
        text = "<b>"+text+"                ."
    if  color == "Random":
        icon = text
        n['tile_color'].setValue(t)
    if sticky == "sticky" and color != "Precomp":
        n = nuke.nodes.StickyNote(note_font_size =font, note_font = 1, label = text, tile_color = 4294967295 )
        n.setXYpos(xMinMaxPos[0]-fontsX,yMinMaxPos[0]-fontsY)

    else:
        n['label'].setValue(text)
    
    if  bookmark == 1:
        n['bookmark'].setValue(1)

    
    if  color == "Red":
        icon = text
        n['tile_color'].setValue(2466250752L)
        Bn['tile_color'].setValue(2466250752L)
        n['label'].setValue(icon)
    if   color == "Green":
        icon = text
        n['tile_color'].setValue(1063467008L)
        Bn['tile_color'].setValue(1063467008L)
        n['label'].setValue(icon)
    if   color == "Blue":
        icon = text
        n['tile_color'].setValue(1027575296L)
        Bn['tile_color'].setValue(1027575296L)
        n['label'].setValue(icon)
    if   color == "Magenta":
        icon =text
        n['tile_color'].setValue(1358974720L)
        Bn['tile_color'].setValue(1358974720L)
        n['label'].setValue(icon)
    if   color== "Cyan":
        icon = text
        n['tile_color'].setValue(861493759)
        Bn['tile_color'].setValue(861493759)
        n['label'].setValue(icon)
    if   color== "Yellow":
        icon = text
        n['tile_color'].setValue(2526413055)
        Bn['tile_color'].setValue(2526413055)
        n['label'].setValue(icon)
    n['selected'].setValue(False)
    # revert to previous selection
    [i['selected'].setValue(True) for i in selNodes]
    
    return n

#autoBackdrop()



