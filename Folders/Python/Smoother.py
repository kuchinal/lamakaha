import nuke
def Smoother():
    
    sh = nuke.selectedNode()
    sh.addKnob(nuke.Array_Knob("sm_gl","smooth global"))
    sh['sm_gl'].setValue(1)
    sh.addKnob(nuke.XYZ_Knob("sm_t","smooth translation"))
    sh['sm_t'].setValue(1)
    sh.addKnob(nuke.XYZ_Knob("sm_r","smooth rotation"))
    sh['sm_r'].setValue(1)
    sh.addKnob(nuke.XYZ_Knob("shaked_translate"))
    sh.addKnob(nuke.XYZ_Knob("shaked_rotate"))
    sh['shaked_translate'].copyAnimations(sh['translate'].animations())
    sh['shaked_rotate'].copyAnimations(sh['rotate'].animations())

    eTx ="shaked_translate.x.integrate(frame-sm_gl*sm_t.x,frame+sm_gl*sm_t.x)/(2*sm_gl*sm_t.x)"
    sh['translate'].setExpression(eTx,0)
    eTy ="shaked_translate.y.integrate(frame-sm_gl*sm_t.y,frame+sm_gl*sm_t.y)/(2*sm_gl*sm_t.y)"
    sh['translate'].setExpression(eTy,1)
    eTz ="shaked_translate.z.integrate(frame-sm_gl*sm_t.z,frame+sm_gl*sm_t.z)/(2*sm_gl*sm_t.z)"
    sh['translate'].setExpression(eTz,2)
    eRx ="shaked_rotate.x.integrate(frame-sm_gl*sm_r.x,frame+sm_gl*sm_r.x)/(2*sm_gl*sm_r.x)"
    sh['rotate'].setExpression(eRx,0)
    eRy ="shaked_rotate.y.integrate(frame-sm_gl*sm_r.y,frame+sm_gl*sm_r.y)/(2*sm_gl*sm_r.y)"
    sh['rotate'].setExpression(eRy,1)
    eRz ="shaked_rotate.z.integrate(frame-sm_gl*sm_r.z,frame+sm_gl*sm_r.z)/(2*sm_gl*sm_r.z)"
    sh['rotate'].setExpression(eRz,2)
    sh['label'].setValue("smoothed")
    sh['tile_color'].setValue(65280L)