



import nuke, nukescripts

def TrackToTransform():

    ###### checking if we are connected to the Tracker node
    try:
        sDude = nuke.selectedNode() 
        sDudeLabel = sDude['label'].evaluate()
        sDudeLabel = sDudeLabel.replace("none ","MM").replace("_","")
        sDudeName = sDude['name'].value()
        if sDude.Class() == "Tracker3" or sDude.Class() == "Tracker4":
            ###### rising th panel and collecting the info
    
            panel=nuke.Panel("transform name")
            panel.addSingleLineInput("name",sDudeLabel)
            panel.addSingleLineInput("range:",'%s-%s' % (nuke.root().firstFrame(),nuke.root().lastFrame()))
            panel.addBooleanCheckBox('bake', True)
            panel.addBooleanCheckBox('clean Transform', False)
            panel.show()
    
            baked = panel.value('bake')
            name = panel.value("name")
            clean = panel.value("clean Transform")
            first = int(panel.value('range:').rpartition("-")[0])
            last = int(panel.value('range:').rpartition("-")[2])+1
            if clean == 0:
                #########check for unique name###################################
                # if panel.value("name") != '':
                #     name = name.replace(' ', '_')
        
                #     nl = []
                #     for nn in nuke.allNodes():
                #         nl.append(nn.name())
                #     if name in nl:
                #         ##########not unique
                #         i = 1
                #         namei = name +'_'+ str(i)
                #         while namei in nl:
                #             namei = name +'_'+ str(i)
                #             i =i+1
                #         name = namei
                    ###########check for unique name done############################
            
                ###### checking which node to create transformNode or transformNodepaint
    
                transformNode = nuke.nodes.Transform()
    
        
                #######setting position of the new node in the graph
                x = int(sDude['xpos'].value())
                y = int(sDude['ypos'].value())
                transformNode.setXYpos(x,y+100)
                if "ref:" not in name:
                    name = name+"\n"+sDudeLabel
                transformNode['label'].setValue(name)
                transformNode['tile_color'].setValue(1836880640)
           
    
    #########################################
    ##############baking the track#################
                if baked is True:
        
                    #########checking the frame range
                    #first = nuke.Root().knob('first_frame').getValue()
                    #first = int(first)
                    #last = nuke.Root().knob('last_frame').getValue()
                    #last = int(last)+1
                    frame = first
                    transformNode['rotate'].setAnimated()
                    transformNode['translate'].setAnimated()
                    transformNode['scale'].setAnimated()
                    transformNode['center'].setAnimated()
                    while frame<last:
                        
                        r = sDude['rotate'].getValueAt(frame)
                        transformNode['rotate'].setValueAt(r,frame)
    
                        tx = sDude['translate'].getValueAt(frame,0)
                        ty = sDude['translate'].getValueAt(frame,1)
                        transformNode['translate'].setValueAt(tx,frame,0)
                        transformNode['translate'].setValueAt(ty,frame,1)
    
                        sx = sDude['scale'].getValueAt(frame,0)
                        sy = sDude['scale'].getValueAt(frame,1)
                        transformNode['scale'].setValueAt(sx,frame,0)
                        transformNode['scale'].setValueAt(sy,frame,1)
    
    
                        cx = sDude['center'].getValueAt(frame,0)
                        cy = sDude['center'].getValueAt(frame,1)
                        transformNode['center'].setValueAt(cx,frame,0)
                        transformNode['center'].setValueAt(cy,frame,1)
                        frame = frame+1
                    transformNode['tile_color'].setValue(1836880640)
                    transformNode.setSelected(True)
                    sDude.setSelected(False)
    
    
    #########################################
    ##############linking the track#################
                else:
    
                    transformNode['rotate'].setExpression("parent."+sDudeName+".rotate")
                    transformNode['translate'].setExpression("parent."+sDudeName+".translate")
                    transformNode['scale'].setExpression("parent."+sDudeName+".scale")
                    transformNode['center'].setExpression("parent."+sDudeName+".center")
    
                    transformNode.setSelected(True)
                    sDude.setSelected(False)
            else:
                nuke.createNode("Transform")
############################################################
############    if the selected node is not a tracker          ############
#############################################################
        else:
            transformNode = nuke.createNode("Transform")
            x = int(sDude['xpos'].value())
            y = int(sDude['ypos'].value())
            if sDude.Class() != "Dot":
                transformNode.setXYpos(x,y+50) 
            else:
                transformNode.setXYpos(x-34,y+50) 
##############################################################
###############    if no node selected

    except:
        #import traceback; traceback.print_exc()
        nuke.createNode("Transform")




def transformThis():
    import nuke  
    try: 
        if 'render_mode' in nuke.selectedNode().knobs(): 
            return nuke.createNode( 'TransformGeo' )
        elif 'Deep' in nuke.selectedNode().Class() and "DeepHoldout" not in nuke.selectedNode()['name'].value() and "DeepToImage" not in nuke.selectedNode()['name'].value(): 
            return nuke.createNode( "DeepTransform")
        else:
            TrackToTransform()  
    except: 
        return TrackToTransform() 
#TrackToTransform()
