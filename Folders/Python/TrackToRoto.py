
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


# Original script by Pete O'Connell extended by Alexey Kuchinsky to loop the script over a frame range.
def getTheCornerpinAsMatrix():

     projectionMatrixTo = nuke.math.Matrix4()
     projectionMatrixFrom = nuke.math.Matrix4()

     #dir(projectionMatrix)
     theCornerpinNode = nuke.selectedNode()
     l = theCornerpinNode['label'].value()
     theNewCornerpinNode = nuke.createNode("CornerPin2D")
     theNewCornerpinNode['transform_matrix'].setAnimated()

     imageWidth = float(theCornerpinNode.width())
     imageHeight = float(theCornerpinNode.height())

     first = nuke.Root().knob('first_frame').getValue()
     first = int(first)
     last = nuke.Root().knob('last_frame').getValue()
     last = int(last)+1
     frame = first
     while frame<last:
         to1x = theCornerpinNode['to1'].valueAt(frame)[0]
         to1y = theCornerpinNode['to1'].valueAt(frame)[1]
         to2x = theCornerpinNode['to2'].valueAt(frame)[0]
         to2y = theCornerpinNode['to2'].valueAt(frame)[1]
         to3x = theCornerpinNode['to3'].valueAt(frame)[0]
         to3y = theCornerpinNode['to3'].valueAt(frame)[1]
         to4x = theCornerpinNode['to4'].valueAt(frame)[0]
         to4y = theCornerpinNode['to4'].valueAt(frame)[1]
    
         from1x = theCornerpinNode['from1'].valueAt(frame)[0]
         from1y = theCornerpinNode['from1'].valueAt(frame)[1]
         from2x = theCornerpinNode['from2'].valueAt(frame)[0]
         from2y = theCornerpinNode['from2'].valueAt(frame)[1]
         from3x = theCornerpinNode['from3'].valueAt(frame)[0]
         from3y = theCornerpinNode['from3'].valueAt(frame)[1]
         from4x = theCornerpinNode['from4'].valueAt(frame)[0]
         from4y = theCornerpinNode['from4'].valueAt(frame)[1]
    
         projectionMatrixTo.mapUnitSquareToQuad(to1x,to1y,to2x,to2y,to3x,to3y,to4x,to4y)
         projectionMatrixFrom.mapUnitSquareToQuad(from1x,from1y,from2x,from2y,from3x,from3y,from4x,from4y)
         theCornerpinAsMatrix = projectionMatrixTo*projectionMatrixFrom.inverse()
         theCornerpinAsMatrix.transpose()
       
         a0 = theCornerpinAsMatrix[0]
         a1 = theCornerpinAsMatrix[1]
         a2 = theCornerpinAsMatrix[2]
         a3 = theCornerpinAsMatrix[3]    
         a4 = theCornerpinAsMatrix[4]
         a5 = theCornerpinAsMatrix[5]
         a6 = theCornerpinAsMatrix[6]
         a7 = theCornerpinAsMatrix[7]   
         a8 = theCornerpinAsMatrix[8]
         a9 = theCornerpinAsMatrix[9]
         a10 = theCornerpinAsMatrix[10]
         a11 = theCornerpinAsMatrix[11]    
         a12 = theCornerpinAsMatrix[12]
         a13 = theCornerpinAsMatrix[13]
         a14 = theCornerpinAsMatrix[14]
         a15 = theCornerpinAsMatrix[15]
    
         theNewCornerpinNode['transform_matrix'].setValueAt(a0,frame,0)
         theNewCornerpinNode['transform_matrix'].setValueAt(a1,frame,1)
         theNewCornerpinNode['transform_matrix'].setValueAt(a2,frame,2)
         theNewCornerpinNode['transform_matrix'].setValueAt(a3,frame,3)    
         theNewCornerpinNode['transform_matrix'].setValueAt(a4,frame,4)
         theNewCornerpinNode['transform_matrix'].setValueAt(a5,frame,5)
         theNewCornerpinNode['transform_matrix'].setValueAt(a6,frame,6)
         theNewCornerpinNode['transform_matrix'].setValueAt(a7,frame,7)    
         theNewCornerpinNode['transform_matrix'].setValueAt(a8,frame,8)
         theNewCornerpinNode['transform_matrix'].setValueAt(a9,frame,9)
         theNewCornerpinNode['transform_matrix'].setValueAt(a10,frame,10)
         theNewCornerpinNode['transform_matrix'].setValueAt(a11,frame,11)
         theNewCornerpinNode['transform_matrix'].setValueAt(a12,frame,12)
         theNewCornerpinNode['transform_matrix'].setValueAt(a13,frame,13)
         theNewCornerpinNode['transform_matrix'].setValueAt(a14,frame,14)
         theNewCornerpinNode['transform_matrix'].setValueAt(a15,frame,15)
         frame = frame + 1
    
     theNewCornerpinNode.setSelected(True)
     theCornerpinNode.setSelected(False)
     theNewCornerpinNode['label'].setValue(l)


def cornerMatrixToPaint():

    first = nuke.Root().knob('first_frame').getValue()
    first = int(first)
    last = nuke.Root().knob('last_frame').getValue()
    last = int(last)+1
    frame = first
    
    cor = nuke.selectedNode()
    x = int(cor['xpos'].value())
    y = int(cor['ypos'].value())
    lab = cor['label'].value()
    Roto = nuke.createNode('Roto')
    Roto['label'].setValue(lab)
    Roto.setXYpos(x,y+50)
    Knobs = Roto['curves']
    root=Knobs.rootLayer
    transform = root.getTransform()
    
       
    while frame<last:

        cm0 = cor['transform_matrix'].getValueAt(frame,0)
        cm1 = cor['transform_matrix'].getValueAt(frame,1)
        cm2 = cor['transform_matrix'].getValueAt(frame,2)
        cm3 = cor['transform_matrix'].getValueAt(frame,3)
        cm4 = cor['transform_matrix'].getValueAt(frame,4)
        cm5 = cor['transform_matrix'].getValueAt(frame,5)
        cm6 = cor['transform_matrix'].getValueAt(frame,6)
        cm7 = cor['transform_matrix'].getValueAt(frame,7)
        cm8 = cor['transform_matrix'].getValueAt(frame,8)
        cm9 = cor['transform_matrix'].getValueAt(frame,9)
        cm10 = cor['transform_matrix'].getValueAt(frame,10)
        cm11 = cor['transform_matrix'].getValueAt(frame,11)
        cm12 = cor['transform_matrix'].getValueAt(frame,12)
        cm13 = cor['transform_matrix'].getValueAt(frame,13)
        cm14 = cor['transform_matrix'].getValueAt(frame,14)
        cm15 = cor['transform_matrix'].getValueAt(frame,15)
        
        matr = transform.getExtraMatrixAnimCurve(0,0) 
        matr.addKey(frame,cm0)  
        matr = transform.getExtraMatrixAnimCurve(0,1) 
        matr.addKey(frame,cm1)  
        matr = transform.getExtraMatrixAnimCurve(0,2) 
        matr.addKey(frame,cm2)  
        matr = transform.getExtraMatrixAnimCurve(0,3) 
        matr.addKey(frame,cm3)  
        matr = transform.getExtraMatrixAnimCurve(0,4) 
        matr.addKey(frame,cm4)  
        matr = transform.getExtraMatrixAnimCurve(0,5) 
        matr.addKey(frame,cm5)  
        matr = transform.getExtraMatrixAnimCurve(0,6) 
        matr.addKey(frame,cm6)  
        matr = transform.getExtraMatrixAnimCurve(0,7) 
        matr.addKey(frame,cm7)  
        matr = transform.getExtraMatrixAnimCurve(0,8) 
        matr.addKey(frame,cm8)  
        matr = transform.getExtraMatrixAnimCurve(0,9) 
        matr.addKey(frame,cm9)  
        matr = transform.getExtraMatrixAnimCurve(0,10) 
        matr.addKey(frame,cm10)  
        matr = transform.getExtraMatrixAnimCurve(0,11) 
        matr.addKey(frame,cm11)  
        matr = transform.getExtraMatrixAnimCurve(0,12) 
        matr.addKey(frame,cm12)  
        matr = transform.getExtraMatrixAnimCurve(0,13) 
        matr.addKey(frame,cm13)  
        matr = transform.getExtraMatrixAnimCurve(0,14) 
        matr.addKey(frame,cm14)  
        matr = transform.getExtraMatrixAnimCurve(0,15) 
        matr.addKey(frame,cm15)                 
        frame = frame+1
    Roto['curves'].changed()
   

def RotoFromTrack():
    try:
        a = nuke.selectedNode()
        if "Tracker" in a.Class():
            TrackToRoto()
        elif "CornerPin" in a.Class() or "CornerPin" in a['name'].value():
            getTheCornerpinAsMatrix()
            cornerMatrixToPaint()
        else:
            nuke.createNode("Roto")
    except:
        import traceback; traceback.print_exc()
        nuke.createNode("Roto") 