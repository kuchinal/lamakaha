import nuke
def randomKnob():
    panel = nuke.Panel("rendomize")
    panel.addSingleLineInput('knob', 'knob')
    panel.addSingleLineInput('range', 'from-to')
    
    panel.show()
    knob = panel.value('knob')
    low = int(panel.value("range").rpartition("-")[0])
    high = int(panel.value("range").rpartition("-")[2])
    print low, high
    
    import random
    a = nuke.selectedNodes()
    for n in a:
        n[knob].setValue(random.randint( low, high))