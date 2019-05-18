def RFR():
    import nuke
    import nukescripts
    import LocaliseThreaded
    LocaliseThreaded.register()
    w = nuke.selectedNodes()
    d = 0
    for guy in w:
        d = d+1
    if d ==1:
        from os import listdir
        WriteNodes = [node for node in nuke.selectedNodes() if node.Class()=='Write']
        for node in nuke.selectedNodes():
            if node.Class() == "Write":
                fullPath = node['file'].getValue()
                folder = fullPath.rpartition("/")[0] 
                try:
                    allFiles =  listdir(folder)
                    all = []
                    for file in allFiles:
                        if ".tmp" not in file:
                            file = file.rpartition(".")[0]
                            file = file.rpartition(".")[2]
                            file = int(file)
                            all.append(file)
                    all.sort()
                    minimum = int(all[0])
                    maximum = int(all[-1])
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
            elif node.Class() == "comp_layers_core":
                readwrites()



        e = nuke.selectedNode()
        x = e['xpos'].value()
        y = e['ypos'].value()
        b = nuke.allNodes("BackdropNode")
        for ba in b:
            xb = int(ba['xpos'].value())
            yb = int(ba['ypos'].value())

################################################################## precomp case

            if xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "Precomp":
                ba['tile_color'].setValue(2466250752L)
                n = nuke.selectedNode()
                x = int(n['xpos'].value())
                y = int(n['ypos'].value())
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
                panel = nuke.Panel("localise?")
                panel.addBooleanCheckBox('localise', False)
                panel.show()
                i = panel.value("localise")
                if i == 1:
                    doLocalise(0)

################################################################## Fie out case

            elif xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "File Out":    #File out stuff
                n = nuke.selectedNode()
                five = nuke.toNode("dot5")
                try:           
                    old = five.dependencies(nuke.INPUTS)[0]
                    xo =int(old['xpos'].value())
                    yo = int(old['ypos'].value())
                    old.setXYpos(xo,yo+100)
                except:
                    xo =int(five['xpos'].value()-34)
                    yo = int(five['ypos'].value()-50)
                n.setXYpos(xo,yo)
                five.setInput(0,n)
                index = n['file'].value().find('_v')
                version =  n['file'].value()[index+1:index+6]
                print version
                n['label'].setValue(version)
                
                ### moving old results down
                a = nuke.allNodes("Read")
                for node in a:
                    y = int(node['ypos'].value())
                    x = int(node['xpos'].value())
                    if x> xo-30 and x< xo+30 and y> yo:
                        node.setXYpos(x,y+60)
                

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


