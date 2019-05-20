def RFRLinux():
    import nuke
    n = nuke.selectedNode()
    x = n['xpos'].value()
    y = n['ypos'].value()
    b = nuke.allNodes("BackdropNode")
    for ba in b:
        xb = ba['xpos'].value()
        yb = ba['ypos'].value()
        if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
            ba['tile_color'].setValue(2466250752L)
            
