import nuke

def AllKnobs():
   b = nuke.selectedNode()
   allKnobs = "ALL KNOBS:\n"
   for i in range (b.getNumKnobs()):
     knob =  b.knob (i).name()
     allKnobs = allKnobs + knob+"\n"
   nuke.message(allKnobs)


