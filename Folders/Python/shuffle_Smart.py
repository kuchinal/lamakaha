

def shuffleCreate():
    import nuke
    try :
        a=nuke.selectedNode()
        r = a['red'].value()
        g = a['green'].value()
        b = a['blue'].value()
        aa = a['alpha'].value()
        if "Shuffle" in a.Class():
            if a['in'].value() == "rgba" and r == "red" and g == "red" and b == "red" and aa == "red" and "reconnect" not in a.knobs():
                a['red'].setValue(1)
                a['green'].setValue(5)
                a['blue'].setValue(5)
                a['alpha'].setValue(5) 
                a['label'].setValue("") 
                a['tile_color'].setValue(2466250752L)     
                
                
                
            elif  a['in'].value() == "rgba" and r == "green" and g == "green" and b == "green" and aa == "green" and "reconnect" not in a.knobs():
                a['red'].setValue(5)
                a['green'].setValue(2)
                a['blue'].setValue(5)
                a['alpha'].setValue(5) 
                a['label'].setValue("") 
                a['tile_color'].setValue(1063467008L)       




            elif  a['in'].value() == "rgba" and r == "blue" and g == "blue" and b == "blue" and aa == "blue" and "reconnect" not in a.knobs():
                a['red'].setValue(5)
                a['green'].setValue(5)
                a['blue'].setValue(3)
                a['alpha'].setValue(5)
                a['label'].setValue("")
                a['tile_color'].setValue(1027575296L)
            
        else:
            nuke.createNode('Shuffle')
        
    
    except:
        nuke.createNode('Shuffle')






def shuffleAlpha():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if a['in'].value() == "rgba" and  r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(4)
                a['green'].setValue(4)
                a['blue'].setValue(4)
                a['alpha'].setValue(4)
                a['label'].setValue("")
                a['tile_color'].setValue(4294967295)    
            elif a['in'].value() == "rgba" and  r == "alpha" and g == "alpha" and b == "alpha" and aa == "alpha" and "reconnect" not in a.knobs():
                a['red'].setValue(5)
                a['green'].setValue(5)
                a['blue'].setValue(5)
                a['alpha'].setValue(4)
                a['label'].setValue("")
                a['tile_color'].setValue(4294967295)               

            else:
                nuke.createNode("Axis") 
        elif a.Class() == "Grade":
            a['channels'].setValue("rgba")
            a['label'].setValue("rgba")
        elif a.Class() == "ColorCorrect":
            a['channels'].setValue("rgba")
            a['label'].setValue("rgba")
        elif a.Class() == "Merge2":
            a['also_merge'].setValue("all")
            a['label'].setValue("all")
        else:
            nuke.createNode("Axis")
            pass            
    except:
        nuke.createNode("Axis") 
        pass

###################################################################################################################################################

def shuffleDepth():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if a['in'].value() == "rgba" and  r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(4)
                a['green'].setValue(4)
                a['blue'].setValue(4)
                a['alpha'].setValue(4)
                a['label'].setValue("")  
                a['in'].setValue("depth") 
                a['tile_color'].setValue(1347506687)              
            else:
                nukescripts.toggle("disable")
        else:
            nukescripts.toggle("disable")           
    except:
        nukescripts.toggle("disable")
        

###################################################################################################################################################

def shuffleRed():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            
            name = a['name'].value()
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            lab = a['label'].value()
            if a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(1)
                a['green'].setValue(1)
                a['blue'].setValue(1)
                a['alpha'].setValue(1) 
                a['label'].setValue("") 
                a['tile_color'].setValue(2466250752L) 

            else:
                nukescripts.create_read()

        elif "ID" in name:
            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Red'].value()
            s = nuke.nodes.Shuffle(name=channel)
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)##################
            matte = 1
            s['tile_color'].setValue(2466250752L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(12)


            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
            t=nuke.Text_Knob("chan",str(a['Achannels'].value())+" red channel")
            s.addKnob(t)
        else:
            nukescripts.create_read()         
    except:
        nukescripts.create_read()

#shuffleRed()

###################################################################################################################################################

def shuffleGreen():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            name = a['name'].value()
            
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if  a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(2)
                a['green'].setValue(2)
                a['blue'].setValue(2)
                a['alpha'].setValue(2) 
                a['label'].setValue("") 
                a['tile_color'].setValue(1063467008L)   
            else:
                nuke.createNode("Grade")
        elif "ID" in name:

            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Green'].value()
            s = nuke.nodes.Shuffle(name=channel)
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)
            matte = 2
            s['tile_color'].setValue(1063467008L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(12)

            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
            t=nuke.Text_Knob("chan",str(a['Achannels'].value())+" green channel")
            s.addKnob(t)
        else:
            nuke.createNode("Grade")         
    except:
        nuke.createNode("Grade")

###################################################################################################################################################

def shuffleBlue():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            
            name = a['name'].value()
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            lab = a['label'].value()
            if  a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha" :
                a['red'].setValue(3)
                a['green'].setValue(3)
                a['blue'].setValue(3)
                a['alpha'].setValue(3)
                a['label'].setValue("")
                a['tile_color'].setValue(1027575296L)

            else:
                nuke.createNode("Blur") 
        elif "ID" in name:
            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Blue'].value()
            s = nuke.nodes.Shuffle(name=channel)
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)
            matte = 3
            s['tile_color'].setValue(1027575296L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(12)

            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
            t=nuke.Text_Knob("chan",str(a['Achannels'].value())+" blue channel")
            s.addKnob(t)
        else:
            nuke.createNode("Blur")                 
    except:
        nuke.createNode("Blur")





