import nuke
def NameMy():
    panel = nuke.Panel("Bold")
    panel.addSingleLineInput("Name:","")
    panel.show()
    name = panel.value("Name:")
    #check for unique name
    nl = []
    for nn in nuke.allNodes():
        nl.append(nn.name())
    if name in nl:
        #not unique
        i = 1
        namei = name +'_'+ str(i)
        while namei in nl:
            namei = name +'_'+ str(i)
            i =i+1
        name = namei
    else:
        namei = name
    #check for unique name done
    n = nuke.selectedNode()
    n['name'].setValue(namei)
    n['note_font'].setValue("Bold")
    n['note_font_size'].setValue(14)
    x = n.xpos()
    y = n.ypos()
    n.setXYpos(x,y-15)
