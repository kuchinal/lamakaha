def cornerMatrixToPaint():
    import nuke
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
    Roto.setXYpos(x,y+50)
#cornerMatrixToPaint()