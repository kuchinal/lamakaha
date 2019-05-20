def k():
    me = nuke.thisKnob()
    frame = nuke.frame()
    me.setAnimated()
    current = me.value()
    me.setValue(current)
    me.setValueAt(0,frame-1)
    me.setValueAt(0,frame+1)

b = nuke.thisNode()
nodeclass = b.Class()
for i in range (b.getNumKnobs()):
    knob =  b.knob (i).name()
    nuke.addKnobChanged(k,nodeclass)
    nuke.removeKnobChanged(k,nodeclass)