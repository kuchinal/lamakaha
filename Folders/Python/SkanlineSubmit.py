
def SkanlineSubmit():
    import nuke
    import submit_nuke
    name = nuke.Root().knob('name').getValue()
    if "autosave" in name:
        nuke.message("<font color='Red'><b>YUO ARE SUBMITING AN AUTOSAVE!!!!")
    all = nuke.allNodes("Read")
    for a in all:
        y = a['file'].value().replace("Inferno2","inferno2")
        a['file'].setValue(y)
    try :
        g = nuke.selectedNode() 
        f = nuke.allNodes("WriteBot")
        for a in f:
            sel = a['selected'].value()
            if sel == 1:
                a['disable'].setValue(0)
            else:
                a['disable'].setValue(1)
        nuke.scriptSave()
        print "selected"
        submit_nuke.RushSubmitDialog()   
        n = nuke.selectedNodes()
        for n in n:
            x = n['xpos'].value()
            y = n['ypos'].value()
            b = nuke.allNodes("BackdropNode")
            for ba in b:
                xb = ba['xpos'].value()
                yb = ba['ypos'].value()
                if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
                    ba['tile_color'].setValue(52479)
                    
    except:
        nuke.scriptSave()
        submit_nuke.RushSubmitDialog()
        print "all"
