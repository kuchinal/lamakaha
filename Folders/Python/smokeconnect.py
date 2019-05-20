def smokeconnect():
    import random
    import nuke
    smokea = nuke.toNode("smokea")
    smokeb = nuke.toNode("smokeb")
    smokec = nuke.toNode("smokec")
    smoked = nuke.toNode("smoked")
    smokee = nuke.toNode("smokee")
    n = nuke.selectedNodes()
    for o in n:
        t = random.randint( 0,4)
        if t == 0:
            o.setInput(0,smokea)
        if t == 1:
            o.setInput(0,smokeb)
        if t == 2:
            o.setInput(0,smokec)
        if t == 3:
            o.setInput(0,smoked)
        if t == 4:
            o.setInput(0,smokee)
    