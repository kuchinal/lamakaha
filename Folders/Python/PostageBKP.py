import nuke
def Postage():
    t= nuke.selectedNodes()
    for t in t:  
        name = t['name'].value() 
        label = t['label'].value()
        color = t['tile_color'].value()
        x = int(t['xpos'].value())
        y = int(t['ypos'].value())
        if t.Class()=="Dot" and "deep" not in str(t.metadata()):

            if "ID" in name:
                channel = t['channel'].value()
                s = nuke.nodes.Shuffle()
                s.setXYpos(x,y+50)
                s.setInput(0,t)
                #s['in'].setValue(layer)
                if "red" in  name:
                    matte = 1
                    s['tile_color'].setValue(2466250752L)
                if "green" in  name:
                    matte = 2
                    s['tile_color'].setValue(1063467008L)
                if "blue" in  name:
                    matte = 3
                    s['tile_color'].setValue(1027575296L)
                s['red'].setValue(matte)
                s['green'].setValue(matte)
                s['blue'].setValue(matte)
                s['alpha'].setValue(matte)
                s['hide_input'].setValue(1)
                s['note_font_size'].setValue(20)
                s['autolabel'].setValue("nuke.thisNode()['label'].value()")
                s['label'].setValue(channel)
                u=s
            else:
                label = t['label'].value()
                x = int(t.xpos())
                y = int(t.ypos())
                y = int(y)
                u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,name = label, hide_input = 1 )
                u.setInput(0,t)
                u.setXYpos(int(x-50),int(y+50))

        elif t.Class()=="Read":
            if t['label'].value() == "":
                u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,label = name, hide_input = 1, name = "____" )
            else:
                u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,label = label, hide_input = 1, name = "____" )
            u.setInput(0,t)
            u.setXYpos(x,y+50)


        elif "Camera" in t.Class():
            if t['label'].value() == "":
                u = nuke.nodes.NoOp(note_font_size =   20, tile_color = 4000,label = name, hide_input = 1, name = "____" )
            else:
                u = nuke.nodes.NoOp(note_font_size =   20, tile_color = 4000, hide_input = 1, name = label )
            u.setInput(0,t)
            u.setXYpos(x,y+100)
            

        elif "deep" in str(t.metadata()) and "depth" not in str(t.channels()) or "DeepMerge" in t['name'].value() or "DeepReformat" in t['name'].value() :
            if t['label'].value() == "":
                u = nuke.nodes.DeepExpression(note_font_size =   20, tile_color = 4000,label = name, hide_input = 1, name = "____" )
            else:
                u = nuke.nodes.DeepExpression(note_font_size =   20, tile_color = 4000, hide_input = 1, name = label )
            u.setInput(0,t)
            u.setXYpos(x,y+100)
            
        else:
            if t['label'].value() == "":         
                u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,name = name, hide_input = 1 )
            else:
                u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,name = label, hide_input = 1 )
            u.setInput(0,t)
            u.setXYpos(x,y+50)
        u['help'].setValue(name)   
        code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
        m = nuke.PyScript_Knob("showsourse","show source",code)
        u.addKnob(m)
        code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
        m = nuke.PyScript_Knob("jumptosource","jump to source",code)
        u.addKnob(m)
        
        code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
        m = nuke.PyScript_Knob("reconnect","reconnect",code)
        u.addKnob(m)


                    


