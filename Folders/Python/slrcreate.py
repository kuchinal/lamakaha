def slrcreate():
    import nuke
    try:
        a = nuke.selectedNode()
        x = int(a["xpos"].value())
        y = int(a["ypos"].value())
        s = nuke.nodes.ScanlineRender()
        if "Camera" in a.Class():
            print "c"
            s.setInput(2,a)
            s.setXYpos(x+100,y+25)
            
        elif "render_mode" in a.knobs():
            print "o"
            s.setInput(1,a)
            s.setXYpos(x,y+70)
        else:
            s.setInput(0,a)
            s.setXYpos(x-120,y)

    except:
        nuke.createNode("ScanlineRender")
        import traceback;traceback.print_exc()
