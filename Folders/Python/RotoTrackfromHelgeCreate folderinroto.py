def RotoTrack():
    import nuke
    import nuke.curvelib
    import nuke.rotopaint as rp

    
    # Trackerlist
    tracker_list = []
    tracker_list_print = ''
    for i in nuke.allNodes('Tracker4'):
        name = i['name'].value()
        tracker_list.append(name)
        tracker_list_print = tracker_list_print + name + ' '
    # check auf Tracker
    if tracker_list_print == '':
        nuke.message('no Trackers found')
        return

    # User Input
    p = nuke.Panel('meins')
    p.addEnumerationPulldown('Select Tracker', tracker_list_print)
    p.addEnumerationPulldown('Matchmove / Stabilize', 'Matchmove Stablilize')
    p.addEnumerationPulldown('Layer', 'Root Layer1')
    p.addEnumerationPulldown('Link / Bake', 'Link Link')
    p.addBooleanCheckBox('Translation', True)
    p.addBooleanCheckBox('Rotation', True)
    p.addBooleanCheckBox('Scale', True)
    p.addBooleanCheckBox('Center', True)
    p.addBooleanCheckBox('Use different Ref Frame?', False)
    p.addExpressionInput('Ref Frame', '0')
    p.show()

    # cancel
    if not p.value('Select Tracker'):
        return

    # variablen von user input
    usr_tracker = p.value('Select Tracker')
    usr_mmstab = p.value('Matchmove / Stabilize')
    usr_layer = p.value('Layer')
    usr_link = p.value('Link / Bake')
    usr_trans = p.value('Translation')
    usr_rot = p.value('Rotation')
    usr_scale = p.value('Scale')
    usr_center = p.value('Center')
    usr_useRef = p.value('Use different Ref Frame?')
    usr_refFrame = str(p.value('Ref Frame'))



    # create new Roto
    r = nuke.createNode('Roto')
    cKnob = r['curves']
    root = cKnob.rootLayer



    ## hier entscheiden, ob auf root oder auf layer1
    if usr_layer == 'Root':
        tf = root.getTransform() 
    if usr_layer == 'Layer1':
        layer = rp.Layer(cKnob)
        root.append(layer)
        tf = layer.getTransform() 


    tf_translate_x = tf.getTranslationAnimCurve(0)
    tf_translate_y = tf.getTranslationAnimCurve(1)
    tf_rotate = tf.getRotationAnimCurve(0)
    tf_scale_x = tf.getScaleAnimCurve(0)
    tf_scale_y = tf.getScaleAnimCurve(1)
    tf_center_x = tf.getPivotPointAnimCurve(0)
    tf_center_y = tf.getPivotPointAnimCurve(1)

    
    if usr_useRef == False:
        
        if usr_layer == 'Root':      
            # werte setzen LINKS ohne CustomRefFrame, nur auf ROOT (simpel)
            if usr_trans == True:
                r['translate'].setExpression('parent.'+usr_tracker+'.translate')
            if usr_rot == True:
                r['rotate'].setExpression('parent.'+usr_tracker+'.rotate')
            if usr_scale == True:
                r['scale'].setExpression('parent.'+usr_tracker+'.scale')
            if usr_center == True:
                r['center'].setExpression('parent.'+usr_tracker+'.center')
            
        if usr_layer == 'Layer1':
            # werte setzen LINKS ohne CustomRefFrame, nur auf Layer1 (simpel)
            t = nuke.createNode('Roto') ## temp container
            
            if usr_trans == True:
                t['translate'].setExpression('parent.'+usr_tracker+'.translate')
            if usr_rot == True:
                t['rotate'].setExpression('parent.'+usr_tracker+'.rotate')
            if usr_scale == True:
                t['scale'].setExpression('parent.'+usr_tracker+'.scale')
            if usr_center == True:
                t['center'].setExpression('parent.'+usr_tracker+'.center')
            
            transObj = t['curves'].rootLayer.getTransform()
            layer.setTransform(transObj)
            nuke.delete(t)

    if usr_useRef == True:
        
        if usr_layer == 'Root':      
            # werte setzen LINKS mit CustomRefFrame, nur auf ROOT (simpel)
            if usr_trans == True:
                r['translate'].setExpression(usr_tracker+'.translate('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_rot == True:
                r['rotate'].setExpression(usr_tracker+'.rotate('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_scale == True:
                r['scale'].setExpression(usr_tracker+'.scale('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_center == True:
                r['center'].setExpression(usr_tracker+'.center('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            
        if usr_layer == 'Layer1':
            # werte setzen LINKS mit CustomRefFrame, nur auf Layer1 (simpel)
            t = nuke.createNode('Roto') ## temp container
            
            if usr_trans == True:
                t['translate'].setExpression(usr_tracker+'.translate('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_rot == True:
                t['rotate'].setExpression(usr_tracker+'.rotate('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_scale == True:
                t['scale'].setExpression(usr_tracker+'.scale('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            if usr_center == True:
                t['center'].setExpression(usr_tracker+'.center('+ usr_tracker + '.reference_frame+frame-'+usr_refFrame+')')
            
            transObj = t['curves'].rootLayer.getTransform()
            layer.setTransform(transObj)
            nuke.delete(t)
