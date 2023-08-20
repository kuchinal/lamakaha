def shuffleBlue():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(3)
                a['green'].setValue(3)
                a['blue'].setValue(3)
                a['alpha'].setValue(3) 
            else:
                nuke.createNode("Blur") 
        else:
            nuke.createNode("Blur")                 
    except:
        nuke.createNode("Blur")


