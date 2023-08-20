import nuke
def Wipe():
    
  
    # Creating requred nodes
    u = nuke.selectedNode()
    b = nuke.createNode('Grid')
    b['number'].setValue([38.4,21.6])
    b['size'].setValue(0.2)
    
    x=u.knob("xpos").value()
    y=u.knob("ypos").value()
    
    left = nuke.nodes.OneView()
    Ltext= nuke.createNode("Text")
    Ltext['message'].setValue("LEFT")
    Ltext['box'].setValue([0,50,0,0])
    Ltext['name'].setValue("Ltext")
    Ltext['hide_input'].setValue(1)
    left['view'].setValue("left")
    left['name'].setValue("left")
    left['hide_input'].setValue(1)

    left.setInput(0,b)
    Ltext.setInput(0,left)
    
    Rtext= nuke.createNode("Text")
    Rtext['message'].setValue("RIGHT")
    Rtext['box'].setValue([0,50,0,0])
    Rtext['name'].setValue("Rtext")
    Rtext['hide_input'].setValue(1)
    Rtext.setInput(0,b)
    Rtext['label'].setValue("Delete After Use")
    right = nuke.createNode('OneView')
    right['view'].setValue("right")
    right['name'].setValue("right")
    right['hide_input'].setValue(1)
    right['label'].setValue("Delete After Use")

    

    
    # Connecting to Viewer
    nuke.connectViewer(0,Ltext)
    nuke.connectViewer(1,right)
    
    #Positioning nodes somewhere :)
    x = int(x)
    y = int(y)
    left.setXYpos(x,y+150)
    right.setXYpos(x,y+150)
    Ltext.setXYpos(x,y+150)
    Rtext.setXYpos(x,y+150)
    b.setXYpos(x,y+150)