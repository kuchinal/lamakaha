def RFRLinux():
    import nuke
    import scanline_utilities 
    scanline_utilities.readFromWrite()
    n = nuke.selectedNode()
    x = n['xpos'].value()
    y = n['ypos'].value()
    b = nuke.allNodes("BackdropNode")
    for ba in b:
        xb = ba['xpos'].value()
        yb = ba['ypos'].value()
        if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
            ba['tile_color'].setValue(2466250752L)
            
def RFR():
    import nuke
    import scanline_utilities 

    w = nuke.selectedNodes()
    d = 0
    for guy in w:
        d = d+1
    if d ==1:
        scanline_utilities.readFromWrite()
        e = nuke.selectedNode()
        x = e['xpos'].value()
        y = e['ypos'].value()
        b = nuke.allNodes("BackdropNode")
        for ba in b:
            xb = ba['xpos'].value()
            yb = ba['ypos'].value()
            if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
                ba['tile_color'].setValue(2466250752L)
                n = nuke.selectedNode()
                x = n['xpos'].value()
                y = n['ypos'].value()
                t = nuke.selectedNode()
                new =  t['name'].value()
                b = nuke.allNodes("Read")
                for a in b:
                    xa = a['xpos'].value()
                    ya = a['ypos'].value()
                    if  xa>x-50 and xa<x+50  and ya>y-50 and ya<y+50 :
                        g = a['name'].value()
                        if new in g:
                            fresh = n
                        else:
                            d = a['name'].value()
                            a.setXYpos(x-200,y)
                d = nuke.allNodes("Dot")
                for dot in d:
                    xa = dot['xpos'].value()
                    ya = dot['ypos'].value()
                    if  xa>x-200 and xa<x+200  and ya>y-200 and ya<y+200 :
                        g = dot['label'].value()
                        if "OUT" in g:
                            dot.setInput(0,fresh)
    
            elif xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "File Out":    #File out stuff
                n = nuke.selectedNode()
                try:
                    five = nuke.toNode("dot5")
                    old = five.dependencies(nuke.INPUTS)[0]
                    xo = old['xpos'].value()
                    yo = old['ypos'].value()
                    nuke.delete(old)
                    n.setXYpos(xo,yo)
                    five.setInput(0,n)
                except:
                    print ""
    else:
        for node in nuke.selectedNodes():
            label = node['label'].value()
            if label == "IN":
                IN = node
            elif label =="OUT":
                OUT = node
            elif label == "Precomp":
                PREC = node
        OUT.setInput(0,IN)
        PREC['tile_color'].setValue(4294967295)
        print "hallo"
                
def RFRBKP():
    import nuke
    import scanline_utilities 
    w = nuke.selectedNode()
    scanline_utilities.readFromWrite()
    e = nuke.selectedNode()
    x = e['xpos'].value()
    y = e['ypos'].value()
    b = nuke.allNodes("BackdropNode")
    for ba in b:
        xb = ba['xpos'].value()
        yb = ba['ypos'].value()
        if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
            ba['tile_color'].setValue(2466250752L)
    n = nuke.selectedNode()
    x = n['xpos'].value()
    y = n['ypos'].value()
    t = nuke.selectedNode()
    new =  t['name'].value()
    b = nuke.allNodes("Read")
    for a in b:
        xa = a['xpos'].value()
        ya = a['ypos'].value()
        if  xa>x-50 and xa<x+50  and ya>y-50 and ya<y+50 :
            g = a['name'].value()
            if new in g:
                fresh = n
            else:
                d = a['name'].value()
                a.setXYpos(x-200,y)
                
'''
                try:
                    rotten = a.dependent()[0]
                    rotten.setInput(0,t)
                except:
                    print w['name'].value()
                    up = w.dependencies(nuke.INPUTS)[0]
                    down = up.dependent()[0]
                    nd =  down['name'].value()
                    if "Write" not in nd:
                        down.setInput(0,t)'''
            
            
       
            
