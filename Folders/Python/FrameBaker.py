def FrameBaker():
    import nuke
    def FrameB(Froze):
        n = nuke.selectedNode()  
        label = n['label'].setValue(Froze)  
        u = 'curve'+'('+ Froze+ ')'
        trans = n['translate']
        if trans.isAnimated():
            n['translate'].setExpression(u)
        else:
            return        
	rot = n['rotate'] 
        if rot.isAnimated():  
            n['rotate'].setExpression(u)
        else:
            return

        foc = n['focal']
        if foc.isAnimated():
            n['focal'].setExpression(u)
        else:
            return
  
        n['tile_color'].setValue(65280L)
        n['gl_color'].setValue(65280L)
        
    frame = nuke.tcl('frame')
    panel = nuke.Panel('Frozen Frame')
    panel.addSingleLineInput("BakedFrame",frame)
    panel.show()
    
    Froze = panel.value('BakedFrame')
    print Froze
    FrameB(Froze)