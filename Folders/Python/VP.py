           
def Saturation():
    import nuke
    w = nuke.allNodes("Viewer")
    t = nuke.toNode("root")['viewer_process']
    f = t.value()
    for one in w:
        val = one['viewerProcess'].value()
        if val  !=  "Saturation":
            t.setValue(val)
            one['viewerProcess'].setValue("Saturation")
        if val ==  "Saturation":
            one['viewerProcess'].setValue(f)
			
def Grid():
    import nuke
    w = nuke.allNodes("Viewer")
    t = nuke.toNode("root")['viewer_process']
    f = t.value()
    for one in w:
        val = one['viewerProcess'].value()
        if val  !=  "Grid":
            t.setValue(val)
            one['viewerProcess'].setValue("Grid")
        if val ==  "Grid":
            one['viewerProcess'].setValue(f)
					
def Flip():
    import nuke
    w = nuke.allNodes("Viewer")
    t = nuke.toNode("root")['viewer_process']
    f = t.value()
    for one in w:
        val = one['viewerProcess'].value()
        if val  !=  "Flip":
            t.setValue(val)
            one['viewerProcess'].setValue("Flip")
        if val ==  "Flip":
            one['viewerProcess'].setValue(f)
			
def Flop():
    import nuke
    w = nuke.allNodes("Viewer")
    t = nuke.toNode("root")['viewer_process']
    f = t.value()
    for one in w:
        val = one['viewerProcess'].value()
        if val  !=  "Flop":
            t.setValue(val)
            one['viewerProcess'].setValue("Flop")
        if val ==  "Flop":
            one['viewerProcess'].setValue(f)