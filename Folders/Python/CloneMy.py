def CloneMy():
    import nuke
    nod = nuke.selectedNode()
    x = int(nod['xpos'].value())
    y = int(nod['ypos'].value())
    nodname = nod['name'].value()
    nod['label'].setValue("Main")
    clas = nod.Class()
    p = nuke.Panel('links')
    list = "disable"
    nod.setSelected(False)

    new = nuke.createNode(clas)
    new.setInput(0,None)
    new['label'].setValue("Child")
    new.setXYpos(x+150,y)



    for i in range (nod.getNumKnobs()):
        name =  nod.knob (i).name()
        list = list +" " +name
        if nod[name].isAnimated():
           new[name].setExpression("parent."+nodname+"."+name)




    if clas == "Transform":
        p.addEnumerationPulldown('Link A', "translate "+list)
        p.addEnumerationPulldown('Link B', "scale "+list)
        p.addEnumerationPulldown('Link C', "skewX "+list)
        p.addEnumerationPulldown('Link D', "skewY "+list)
        p.addEnumerationPulldown('Link E', "skew_order "+list)
        p.addEnumerationPulldown('Link F', "center "+list)
        p.addEnumerationPulldown('Link G', "filter "+list)
        p.addEnumerationPulldown('Link H', "motionblur "+list)
        p.addEnumerationPulldown('Link I', "shutter "+list)
        p.addEnumerationPulldown('Link K', "rotate "+list)
        p.addEnumerationPulldown('Link L', "disable "+list)
        p.addEnumerationPulldown('Link M', "disable "+list)
        p.addEnumerationPulldown('Link N', "disable "+list)



    elif clas == "Tracker4":
        p.addEnumerationPulldown('Link A', "translate "+list)
        p.addEnumerationPulldown('Link B', "scale "+list)
        p.addEnumerationPulldown('Link C', "skewX "+list)
        p.addEnumerationPulldown('Link D', "skewY "+list)
        p.addEnumerationPulldown('Link E', "skew_order "+list)
        p.addEnumerationPulldown('Link F', "center "+list)
        p.addEnumerationPulldown('Link G', "filter "+list)
        p.addEnumerationPulldown('Link H', "motionblur "+list)
        p.addEnumerationPulldown('Link I', "shutter "+list)
        p.addEnumerationPulldown('Link K', "rotate "+list)
        p.addEnumerationPulldown('Link L', "reference_frame "+list)
        p.addEnumerationPulldown('Link M', "transform "+list)
        p.addEnumerationPulldown('Link N', "jitter_period "+list)


    elif clas == "CornerPin2D":
        p.addEnumerationPulldown('Link A', "to1 "+list)
        p.addEnumerationPulldown('Link B', "to2 "+list)
        p.addEnumerationPulldown('Link C', "to3 "+list)
        p.addEnumerationPulldown('Link D', "to4 "+list)
        p.addEnumerationPulldown('Link E', "help "+list)
        p.addEnumerationPulldown('Link F', "help "+list)
        p.addEnumerationPulldown('Link G', "help "+list)
        p.addEnumerationPulldown('Link H', "help "+list)
        p.addEnumerationPulldown('Link I', "help "+list)
        p.addEnumerationPulldown('Link K', "help "+list)
        p.addEnumerationPulldown('Link L', "help "+list)
        p.addEnumerationPulldown('Link M', "help "+list)
        p.addEnumerationPulldown('Link N', "help "+list)
    elif clas == "Grade":
        p.addEnumerationPulldown('Link A', "blackpoint "+list)
        p.addEnumerationPulldown('Link B', "whitepoint "+list)
        p.addEnumerationPulldown('Link C', "black "+list)
        p.addEnumerationPulldown('Link D', "white "+list)
        p.addEnumerationPulldown('Link E', "multiply "+list)
        p.addEnumerationPulldown('Link F', "add "+list)
        p.addEnumerationPulldown('Link G', "gamma "+list)
        p.addEnumerationPulldown('Link H', "mix "+list)
        p.addEnumerationPulldown('Link I', "channels "+list)
        p.addEnumerationPulldown('Link K', "disable "+list)
        p.addEnumerationPulldown('Link L', "disable "+list)
        p.addEnumerationPulldown('Link M', "disable "+list)
        p.addEnumerationPulldown('Link N', "disable "+list)
    elif clas == "ColorCorrect":
        p.addEnumerationPulldown('Link A', "saturation "+list)
        p.addEnumerationPulldown('Link B', "contrast "+list)
        p.addEnumerationPulldown('Link C', "gamma "+list)
        p.addEnumerationPulldown('Link D', "gain "+list)
        p.addEnumerationPulldown('Link E', "offset "+list)
        p.addEnumerationPulldown('Link F', "highlights.gain "+list)
        p.addEnumerationPulldown('Link G', "shadows.gain "+list)
        p.addEnumerationPulldown('Link H', "mix "+list)
        p.addEnumerationPulldown('Link I', "channels "+list)
        p.addEnumerationPulldown('Link K', "disable "+list)
        p.addEnumerationPulldown('Link L', "disable "+list)
        p.addEnumerationPulldown('Link M', "disable "+list)
        p.addEnumerationPulldown('Link N', "disable "+list)
    else:
        p.addEnumerationPulldown('Link A', list)
        p.addEnumerationPulldown('Link B', list)
        p.addEnumerationPulldown('Link C', list)
        p.addEnumerationPulldown('Link D', list)
        p.addEnumerationPulldown('Link E', list)
        p.addEnumerationPulldown('Link F', list)
        p.addEnumerationPulldown('Link G', list)
        p.addEnumerationPulldown('Link H', list)
        p.addEnumerationPulldown('Link I', list)
        p.addEnumerationPulldown('Link K', list)
        p.addEnumerationPulldown('Link L', list)
        p.addEnumerationPulldown('Link M', list)
        p.addEnumerationPulldown('Link N', list)

    p.show()

    A = p.value('Link A')
    B = p.value('Link B')
    C = p.value('Link C')
    D = p.value('Link D')
    E = p.value('Link E')
    F = p.value('Link F')
    G = p.value('Link G')
    H = p.value('Link H')
    I= p.value('Link I')
    K = p.value('Link K')
    L = p.value('Link L')
    M = p.value('Link M')
    N = p.value('Link N')

    new[A].setExpression("parent."+nodname+"."+A)
    new[B].setExpression("parent."+nodname+"."+B)
    new[C].setExpression("parent."+nodname+"."+C)
    new[D].setExpression("parent."+nodname+"."+D)
    new[E].setExpression("parent."+nodname+"."+E)
    new[F].setExpression("parent."+nodname+"."+F)
    new[G].setExpression("parent."+nodname+"."+G)
    new[H].setExpression("parent."+nodname+"."+H)
    new[I].setExpression("parent."+nodname+"."+I)
    new[K].setExpression("parent."+nodname+"."+K)
    new[L].setExpression("parent."+nodname+"."+L)
    new[M].setExpression("parent."+nodname+"."+M)
    new[N].setExpression("parent."+nodname+"."+N)
    



