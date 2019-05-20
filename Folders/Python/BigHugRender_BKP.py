def BigHugRender():
    import bhfx.nuke.submitrender
    nuke.scriptSave()
    try :
        g = nuke.selectedNode()
        f = nuke.allNodes("Write")+nuke.allNodes("DeepWrite")
        for a in f:
            sel = a['selected'].value()
            names = ""
            if sel == 1:
                a['disable'].setValue(0)
                name = a['name'].value()
                names = names + name+"\n"
            else:
                a['disable'].setValue(1)
        bhfx.nuke.submitrender.launch()
    except:
        bhfx.nuke.submitrender.launch()

    try:
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
        bhfx.nuke.submitrender.launch()