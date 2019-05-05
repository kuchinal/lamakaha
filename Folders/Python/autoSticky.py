

# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
#
# This example will automatically put a backdrop behind the selected nodes
#

import nuke, operator, random

def autoSticky():

    panel=nuke.Panel("Sticky Name")
    panel.addSingleLineInput("Label","")
    panel.addEnumerationPulldown("Font", "big huge middle small tiny")
    panel.addEnumerationPulldown("Color", "White Black Red Green Blue Magenta Cyan Yellow")
    panel.addBooleanCheckBox('Bold', True)
    panel.setWidth(400)
    panel.show()


    color = panel.value('Color')
    text = panel.value('Label')
    bookmark = panel.value('bookmark')
    fontA = panel.value('Font')
    fonts = {'big':100, 'huge':300, 'middle':50, 'small':20, 'tiny':10}
    colors = {"White" : 4294967295, "Black" : 255,"Red" : 2466250752L, "Green" : 1063467008L, "Blue" : 1027575296L, "Magenta" : 1358974720L, "Cyan" : 861493759, "Yellow" : 2526413055, }
    font = fonts[fontA]
    color = colors[color]
    bold = panel.value('Bold')


    n = nuke.createNode("StickyNote")
    n['note_font_size'].setValue(font)
    n['bookmark'].setValue(0)
    if bold == True:
        text = "<b>"+text+"                ."

    n['label'].setValue(text)

    n['tile_color'].setValue(color)







