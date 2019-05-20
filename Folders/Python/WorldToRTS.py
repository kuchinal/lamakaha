def consolidateAnimatedNodeTransforms():
    # This is based on Ivan B's consolidateNodeTransforms().
    # Added support for animated Axis/Camera nodes. Also, if it's
    # a Camera being concatenated, then projection settings get copied.
    # -Ean C 24/Feb/2011
    import math
    import nuke
    axisNode = nuke.selectedNode()
    m = nuke.math.Matrix4()


    n = nuke.createNode("Card2")
    n['scaling'].setExpression('curve')
    n['rotate'].setExpression('curve')
    n['translate'].setExpression('curve')

    if axisNode.Class() == 'Camera2':
        # If this is a Camera node, copy over important Projection settings.
        camNode = axisNode

        # Get the current values
        focal_v = camNode['focal'].toScript()
        haperture_v = camNode['haperture'].toScript()
        vaperture_v = camNode['vaperture'].toScript()
        near_v = camNode['near'].toScript()
        far_v = camNode['far'].toScript()
        win_translate_v = camNode['win_translate'].toScript()
        win_scale_v = camNode['win_scale'].toScript()
        winroll_v = camNode['winroll'].toScript()
        focal_point_v = camNode['focal_point'].toScript()

        # Copy them over to new Camera
        n['focal'].fromScript(focal_v)
        n['haperture'].fromScript(haperture_v)
        n['vaperture'].fromScript(vaperture_v)
        n['near'].fromScript(near_v)
        n['far'].fromScript(far_v)
        n['win_translate'].fromScript(win_translate_v)
        n['win_scale'].fromScript(win_scale_v)
        n['winroll'].fromScript(winroll_v)
        n['focal_point'].fromScript(focal_point_v)

    first_frame_v = nuke.root()['first_frame'].value()
    last_frame_v = nuke.root()['last_frame'].value()

    scale_anim = n['scaling'].animations()
    rotate_anim = n['rotate'].animations()
    translate_anim = n['translate'].animations()

    for i in range(int(first_frame_v), int(last_frame_v+1)):

        k = axisNode['world_matrix']
        k_time_aware = axisNode['world_matrix'].getValueAt(i)


        for y in range(k.height()):
            for x in range(k.width()):
                m[x+(y*k.width())] = k_time_aware[y + k.width()*x]


            transM =nuke.math.Matrix4(m)
            transM.translationOnly()
            rotM = nuke.math.Matrix4(m)
            rotM.rotationOnly()
            scaleM = nuke.math.Matrix4(m)
            scaleM.scaleOnly()

            scale = (scaleM.xAxis().x, scaleM.yAxis().y, scaleM.zAxis().z)

            rot = rotM.rotationsZXY()
            rotDegrees = ( math.degrees(rot[0]), math.degrees(rot[1]), math.degrees(rot[2]) )


            trans = (transM[12], transM[13], transM[14])

            for s in range(3):
                scale_anim[s].setKey(i, scale[s])
                rotate_anim[s].setKey(i, rotDegrees[s])
                translate_anim[s].setKey(i, trans[s])

