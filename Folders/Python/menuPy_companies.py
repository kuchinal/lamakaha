if arriVFX == 1:
    import ARRIsubmit

if BlackSailVFX == 1:

    def ScriptNameMenu(): 
        Name.NameBlackSail()
        nuke.scriptSave()
    def ScriptNameMenuUp():
        nukescripts.script_version_up()
        nuke.scriptSave()
        Name.NameBlackSail()

    def RFR_blackSail():
            import nuke
            import nukescripts
            w = nuke.selectedNodes()
            d = 0
            for guy in w:
                d = d+1
            if d ==1:
                getReadFromWrite.getReadFromWrite()
            
                e = nuke.selectedNode()
                x = int(e['xpos'].value())
                y = int(e['ypos'].value())
                e.setXYpos(x,y-25)
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
                        doLocalise(0)
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
                            doLocalise(0)
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
                
    def BlackSailRender():
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
                    #nuke.toNode("Review")['senttorender'].setValue(names)
                else:
                    a['disable'].setValue(1)
                
            BlackSailSubmit.BlackSailSubmit()
        except:
            BlackSailSubmit.BlackSailSubmit()

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
            BlackSailSubmit.BlackSailSubmit()
        
            
            
            
    m=nuke.menu('Nuke')
    n = m.addMenu('RRender')
    import BlackSailSubmit
    n.addCommand('Submit comp', "BlackSailRender()","Alt+f7")
    n.addCommand( 'Read from Write', 'RFR_blackSail()', 'alt+r' )
    n.addCommand('Name', 'ScriptNameMenu()',"Ctrl+s",icon = "my.png")
    n.addCommand('NameUp','ScriptNameMenuUp()',"Alt+Shift+s",icon = "my.png") 



if BigHugVFX==1:        
        
    m=nuke.menu('Nuke')
    n = m.addMenu('BigHug',icon = "easymaker_icon.png")
    n.addCommand('Submit comp alexey', "BigHugRender()","Alt+f7")
    n.addCommand('ReadFromWrite', "RFRBigHug()","Alt+r")
    n.addCommand('Name', 'ScriptNameMenuBigHug()',"Ctrl+s",icon = "my.png")
    n.addCommand('NameUp','ScriptNameMenuUpBigHug()',"Alt+Shift+s",icon = "my.png") 
    n.addCommand('Set people','set()',icon = "my.png")
    n.addCommand('Reconnect people','reconnect()',icon = "my.png")
    #nuke.addOnScriptLoad(latestBigHug)



#######################scanline renders submitters:
def SCrendWindows():
    import nuke
    panel = nuke.Panel("Priority")
    panel.addEnumerationPulldown("priority:", "medium low high")
    if panel.show():
        priority = panel.value("priority:")
    try :
        allNames = ""
        g = nuke.selectedNode() 
        f = nuke.allNodes("comp_layers_core")
        for a in f:
            sel = a['selected'].value()
            if sel == 1:
                a['disable'].setValue(0)
                name = a['layer'].value()+ "---" + a['name'].value()
                allNames = allNames + name + '\n'
            else:
                a['disable'].setValue(1)
        nuke.toNode('LastRender')['message'].setValue(allNames)

        f = nuke.allNodes("Write")
        for a in f:
            sel = a['selected'].value()
            if sel == 1:
                a['disable'].setValue(0)
                name = a['name'].value()
                allNames = allNames + name + '\n'
            else:
                a['disable'].setValue(1)
        nuke.scriptSave()
        nuke.toNode('LastRender')['message'].setValue(allNames)
        w = nuke.allNodes("Viewer")
        for one in w:
            one['input_process_node'].setValue('LastRender')
            val = one['input_process'].value()
            if val  == 0 :
                one['input_process'].setValue(1)
            else:
                one['input_process'].setValue(0)   
        ScanlineCoreSubmitRendering(priority, True, True)
        one['input_process'].setValue(0)

    except:
        nuke.scriptSave()
        ScanlineCoreSubmitRendering(priority, True, True)
        

def SCrendLinux():
    import nuke
    panel = nuke.Panel("Priority")
    panel.addEnumerationPulldown("priority:", "medium low high")
    if panel.show():
        priority = panel.value("priority:")
    try :
        f = nuke.allNodes()
        for a in f:
            if a.Class() == "comp_layers_core" or a.Class() == "Write":
                sel = a['selected'].value()
                if sel == 1:
                    a['disable'].setValue(0)
                else:
                    a['disable'].setValue(1)
        
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
                    
        ScanlineCoreSubmitRendering(priority, True, True)
    except:
        nuke.scriptSave()
        ScanlineCoreSubmitRendering(priority, True, True) 
        
        
def RFRScanlineLinux():
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

            ################################################################# precomp case

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

if scanlineVFXlinux == 1:
    
    m=nuke.menu('Nuke')
    #m.addCommand('name', 'ScriptNameMenu()')
    import openurl
    n = m.addMenu('',icon = "Time1.png")
    n.addCommand('SCrendLinux', 'SCrendLinux()',"Alt+f7",icon = "scanline.png")
    n.addCommand('RV_Jpeg', 'RV.RVlinuxJPEG()',"Alt+f",icon = "rv.png")
    n.addCommand('RV_EXR', 'RV.RVlinuxEXR()',"Alt+Shift+f",icon = "rv.png")
    n.addCommand("ScanlineLayerSet", "nuke.nodePaste(UserDir+'/GeneralSetups/ScanlineLayerSet.nk')")
    n.addCommand("IDpicker", "nuke.nodePaste(UserDir+'/GeneralSetups/IDpicker.nk')")
    n.addCommand("comp_layers_core", "nuke.createNode ('comp_layers_core')","Shift+w",icon="Calculator.png")
    n.addCommand('ReadfromWrite', "RFRScanlineLinux()","Alt+r")

if scanlineVFXwindows == 1:
    import SkanlineSubmit
    nuke.knobDefault('Root.format',infinite_2K)
    nuke.knobDefault('Root.fps','25') 
    m=nuke.menu('Nuke')
    n = m.addMenu('',icon = "Time1.png")
    n.addCommand('ScanlineSubmit', 'SkanlineSubmit.SkanlineSubmit()',"Alt+f7",icon = "ScanlineRender.png")
    n.addCommand('RVexr', 'RV.RVwindowsEXR()',"Alt+Shift+f",icon = "rv.png")
    n.addCommand('RVjpeg', 'RV.RVwindowsJpeg()',"Alt+f",icon = "rv.png")
    n.addCommand('EditRef', 'nukescripts.start("//inferno2/projects/infinite/editorial/")')
    n.addCommand('Version down', "nukescripts.version_down()","Alt+Down")
    n.addCommand('Version up', "nukescripts.version_up()","Alt+Up")
    n.addCommand('ReadfromWrite', "readFromWriteScanline.RFR()","Alt+r")    



def ScriptNameMenuBigHug(): 
    Name.NameBigHug()
    nuke.scriptSave()
def ScriptNameMenuUpBigHug():
    nukescripts.script_version_up()
    nuke.scriptSave()
    Name.NameBigHug()

def latestBigHugBKP():  
    try:
        name = nuke.toNode("root")['name'].value()
        path = name.rpartition("/")[0]
        content=os.listdir(path)
        low = 0
        for item in content:
            if "comp_v" in item and "autosave" not in item and "~" not in item:
                version = int(item.rpartition('_')[2].rpartition('.')[0].rpartition('v')[2])
                if version > low:
                    low = version
        low =  "%03d" % low
        latest = name.rpartition('_')[0]+"_comp_v"+str(low)+".nk"
        nuke.scriptOpen(latest)
        nuke.scriptClose()
    except:
        print "hallo"

def latestBigHug():    
        name = nuke.toNode("root")['name'].value()
        if '.nk' not in name:
            latest = name.rpartition('/')[0]
            nuke.scriptOpen()
            nuke.scriptClose()

def NameBigHug():
    import nuke
    nkFullPath = nuke.Root().knob('name').getValue()
    Name = nkFullPath.split("/")[9]
    Name = Name.split(".")[0]
    m=nuke.menu('Nuke')
    u = m.addMenu(Name)
    print Name

def BigHugRender():
    import bhfx.nuke.submitrender
    nuke.scriptSave()
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

def RFRBigHug():
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
            panel = nuke.Panel("localise?")
            panel.addBooleanCheckBox('localise', False)
            panel.show()
            i = panel.value("localise")
            if i == 1:
                doLocalise(0)

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
                #autolabelOverride.autolabelOverride()
                five.setInput(0,n)
                index = n['file'].value().find('_v')
                version =  n['file'].value()[index+1:index+5]
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

