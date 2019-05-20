import nuke
def Patcher_():
    a = nuke.createNode("Patcher")
    x = int(a['xpos'].value())
    y = int(a['ypos'].value())
    #a = nuke.nodes."Roto"()
    #a.setXYpos(x+50,y)
    a['from_frame'].setValue(nuke.frame())
    a['to_frame'].setValue(nuke.frame())
    a['cloneframe'].setValue(nuke.frame())
    
    
    g = nuke.toNode("root")['format'].value()
    w = g.width()
    h = g.height()
    a['center'].setValue([w/2,h/2])
    
    
    a['point1'].setAnimated()
    a['point2'].setAnimated()
    a['point3'].setAnimated()
    a['point4'].setAnimated()
    a['point1'].setValue([w/2-100,h/2-100])
    a['point2'].setValue([w/2+100,h/2-100])
    a['point3'].setValue([w/2+100,h/2+100])
    a['point4'].setValue([w/2-100,h/2+100])
    #a['shape'].setValue(1)
    #a['disable'].setExpression('from_frame<=frame&&frame<=to_frame?0:1')
    
    
    
    


