def RFRMy():
    import nuke
    import nukescripts
    w = nuke.selectedNodes()
    d = 0
    for guy in w:
        d = d+1
    if d ==1:

        from os import listdir
        WriteNodes = [node for node in nuke.selectedNodes() if node.Class()=='Write']
        for node in nuke.selectedNodes():
            fullPath = node['file'].getValue()
            folder = fullPath.rpartition("/")[0] 
            try:
                allFiles =  listdir(folder)
                all = []
                for file in allFiles:
                    file = file.rpartition(".")[0]
                    file = file.rpartition(".")[2]
                    file = int(file)
                    all.append(file)
                all.sort()
                minimum = all[0]
                maximum = all[-1]
            except:
                minimum = nuke.root()['first_frame'].getValue()
                maximum = nuke.root()['last_frame'].getValue()
                nuke.message("Cant find directory")

            readNode = nuke.createNode('Read')
            readNode['file'].setValue(fullPath)
            readNode['xpos'].setValue(node['xpos'].getValue())
            readNode['ypos'].setValue(node['ypos'].getValue()+85)

            readNode['first'].setValue(minimum)
            readNode['last'].setValue(maximum)
            readNode['origfirst'].setValue(minimum)
            readNode['origlast'].setValue(maximum)
    
        e = nuke.selectedNode()
        x = e['xpos'].value()
        y = e['ypos'].value()
        b = nuke.allNodes("BackdropNode")
        for ba in b:
            xb = int(ba['xpos'].value())
            yb = int(ba['ypos'].value())
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
        
        
        
def RFRScanlineWindows():
    import nuke
    import nukescripts
    w = nuke.selectedNodes()
    d = 0
    for guy in w:
        d = d+1
    if d ==1:

        from os import listdir
        WriteNodes = [node for node in nuke.selectedNodes() if node.Class()=='WriteBot']
        for node in nuke.selectedNodes():
            fullPath = node['file'].getValue()
            folder = fullPath.rpartition("/")[0] 
            try:
                allFiles =  listdir(folder)
                all = []
                for file in allFiles:
                    file = file.rpartition(".")[0]
                    file = file.rpartition(".")[2]
                    file = int(file)
                    all.append(file)
                all.sort()
                minimum = all[0]
                maximum = all[-1]
            except:
                minimum = int(nuke.root()['first_frame'].getValue())
                maximum = int(nuke.root()['last_frame'].getValue())
                nuke.message("Cant find directory")

            readNode = nuke.createNode('Read')
            readNode['file'].setValue(fullPath)
            readNode['xpos'].setValue(int(node['xpos'].getValue()))
            readNode['ypos'].setValue(int(node['ypos'].getValue()+85))

            readNode['first'].setValue(minimum)
            readNode['last'].setValue(maximum)
            readNode['origfirst'].setValue(minimum)
            readNode['origlast'].setValue(maximum)
    
        e = nuke.selectedNode()
        x = e['xpos'].value()
        y = e['ypos'].value()
        b = nuke.allNodes("BackdropNode")
        for ba in b:
            xb = int(ba['xpos'].value())
            yb = int(ba['ypos'].value())
            if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
                ba['tile_color'].setValue(2466250752L)
                n = nuke.selectedNode()
                x = int(n['xpos'].value())
                y = int(n['ypos'].value())
                t = nuke.selectedNode()
                new =  t['name'].value()
                b = nuke.allNodes("Read")
                for a in b:
                    xa = int(a['xpos'].value())
                    ya = int(a['ypos'].value())
                    if  xa>x-50 and xa<x+50  and ya>y-50 and ya<y+50 :
                        g = a['name'].value()
                        if new in g:
                            fresh = n
                        else:
                            d = a['name'].value()
                            a.setXYpos(x-200,y)
                d = nuke.allNodes("Dot")
                for dot in d:
                    xa = int(dot['xpos'].value())
                    ya = int(dot['ypos'].value())
                    if  xa>x-200 and xa<x+200  and ya>y-200 and ya<y+200 :
                        g = dot['label'].value()
                        if "OUT" in g:
                            dot.setInput(0,fresh)
    
            elif xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "File Out":    #File out stuff
                n = nuke.selectedNode()
                try:
                    five = nuke.toNode("dot5")
                    old = five.dependencies(nuke.INPUTS)[0]
                    xo = int(old['xpos'].value())
                    yo = int(old['ypos'].value())
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


