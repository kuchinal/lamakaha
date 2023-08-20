def ripple():
    import nuke
    w = nuke.allNodes("Viewer")
    t = nuke.toNode("root")['viewer_process']
    f = t.value()
    for one in w:
        val = one['viewerProcess'].value()
        if val  !=  "RippleEdit":
            t.setValue(val)
            one['viewerProcess'].setValue("RippleEdit")
        if val ==  "RippleEdit":
            one['viewerProcess'].setValue(f)