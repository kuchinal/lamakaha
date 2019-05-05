



import nuke, nukescripts, nuke.rotopaint as rp, _curvelib as cl

def TrackToRoto():

    ###### checking if we are connected to the Tracker node
    try:
        sDude = nuke.selectedNode() 
        sDudeLabel = sDude['label'].evaluate()
        sDudeLabel = sDudeLabel.replace("none ","MM").replace("_","")
        sDudeName = sDude['name'].value()
        if sDude.Class() == "Tracker3" or sDude.Class() == "Tracker4":###### rising th panel and collecting the info

            panel=nuke.Panel("roto name")
            panel.addSingleLineInput("name",sDudeLabel)
            panel.addSingleLineInput("range:",'%s-%s' % (nuke.root().firstFrame(),nuke.root().lastFrame()))
            panel.addBooleanCheckBox('bake', True)
            panel.addBooleanCheckBox('create RotoPaint', False)
            panel.show()
    
            kind = panel.value("create RotoPaint")
            baked = panel.value('bake')
            name = panel.value("name")
            first = int(panel.value('range:').rpartition("-")[0])
            last = int(panel.value('range:').rpartition("-")[2])+1

            if "ref:" not in name:
                name = name+"\n"+sDudeLabel

            ###### checking which node to create roto or rotopaint
            if kind == 1:
                roto = nuke.nodes.RotoPaint()
            else:    
                roto = nuke.nodes.Roto()
            roto['label'].setValue(name)
            #######setting position of the new node in the graph
            x = int(sDude['xpos'].value())
            y = int(sDude['ypos'].value())
            roto.setXYpos(x,y+100) 
            roto['tile_color'].setValue(11632127)
            roto['cliptype'].setValue("no clip")
            m = nuke.Text_Knob("","","<font color='DaimGray'><b> Created with TrackToRoto. ",)
            roto.addKnob(m)
 
            if baked is True:##############baking the track#################
    
                #########checking the frame range
                #first = nuke.Root().knob('first_frame').getValue()
                #first = int(first)
                #last = nuke.Root().knob('last_frame').getValue()
                #last = int(last)+1
                frame = first
    
                #######acsessing the roto guts
                Knobs = roto['curves']
                root=Knobs.rootLayer
                transform = root.getTransform()
    
                while frame<last:
                    r = sDude['rotate'].getValueAt(frame,0)
                    rr = transform.getRotationAnimCurve(2)
                    rr.addKey(frame,r)
                    tx = sDude['translate'].getValueAt(frame,0)
                    translx = transform.getTranslationAnimCurve(0)
                    translx.addKey(frame,tx)
                    ty = sDude['translate'].getValueAt(frame,1)
                    transly = transform.getTranslationAnimCurve(1)
                    transly.addKey(frame,ty)
                    sx = sDude['scale'].getValueAt(frame,0)
                    ssx = transform.getScaleAnimCurve(0)
                    ssx.addKey(frame,sx)
                    sy = sDude['scale'].getValueAt(frame,1)
                    ssy = transform.getScaleAnimCurve(1)
                    ssy.addKey(frame,sy)
                    cx = sDude['center'].getValueAt(frame,0)
                    ccx = transform.getPivotPointAnimCurve(0)
                    ccx.addKey(frame,cx)
                    cy = sDude['center'].getValueAt(frame,1)
                    ccy = transform.getPivotPointAnimCurve(1)
                    ccy.addKey(frame,cy)
                    frame = frame+1
    
                roto['tile_color'].setValue(9658367)
                roto.setSelected(True)
                sDude.setSelected(False)
            else:##############linking the track#################

                roto['tile_color'].setValue(11645695)

       
                curves_knob = roto["curves"]
                stab_layer = rp.Layer(curves_knob)
                stab_layer.name = "stab_"+sDudeName
            
                trans_curve_x = cl.AnimCurve()
                trans_curve_y = cl.AnimCurve()
            
                trans_curve_x.expressionString = "parent.{0}.translate.x".format(sDudeName)
                trans_curve_y.expressionString = "parent.{0}.translate.y".format(sDudeName)
                trans_curve_x.useExpression = True
                trans_curve_y.useExpression = True
            
                rot_curve = cl.AnimCurve()
                rot_curve.expressionString = "parent.{0}.rotate".format(sDudeName)
                rot_curve.useExpression = True
            
                scale_curve = cl.AnimCurve()
                scale_curve.expressionString = "parent.{0}.scale".format(sDudeName)
                scale_curve.useExpression = True
            
                center_curve_x = cl.AnimCurve()
                center_curve_y = cl.AnimCurve()
                center_curve_x.expressionString = "parent.{0}.center.x".format(sDudeName)
                center_curve_y.expressionString = "parent.{0}.center.y".format(sDudeName)
                center_curve_x.useExpression = True
                center_curve_y.useExpression = True
            
                # Define variable for accessing the getTransform()
                transform_attr = stab_layer.getTransform()
                # Set the Animation Curve for the Translation attribute to the value of the previously defined curve, for both x and y
                transform_attr.setTranslationAnimCurve(0, trans_curve_x)
                transform_attr.setTranslationAnimCurve(1, trans_curve_y)
                # Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
                # http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
                transform_attr.setRotationAnimCurve(2, rot_curve)
                transform_attr.setScaleAnimCurve(0, scale_curve)
                transform_attr.setScaleAnimCurve(1, scale_curve)
                transform_attr.setPivotPointAnimCurve(0, center_curve_x)
                transform_attr.setPivotPointAnimCurve(1, center_curve_y)
                curves_knob.rootLayer.append(stab_layer)

                roto.setSelected(True)
                sDude.setSelected(False)
            roto['curves'].changed()
        else:############    if the selected node is not a tracker          ############
            roto = nuke.createNode("Roto")
            x = int(sDude['xpos'].value())
            y = int(sDude['ypos'].value())
            roto.setXYpos(x,y+50) 
            roto['hide_input'].setValue(0)
##############################################################
###############    if no node selected
        
    except:
        import traceback; traceback.print_exc()
        nuke.createNode("Roto")

#TrackToRoto()

