def disconnect():
    import nuke
    n = nuke.allNodes('Viewer')
    for v in n:
        v.setSelected(True)
        x=v['xpos'].value()
        y=v['ypos'].value()
        nuke.extractSelected()
        v.setXYpos(x,y)
        v.setSelected(False)