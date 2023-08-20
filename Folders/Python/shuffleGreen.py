def shuffleGreen():
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
                a['red'].setValue(2)
                a['green'].setValue(2)
                a['blue'].setValue(2)
                a['alpha'].setValue(2)
            else:
                nuke.createNode("Grade") 
        else:
            nuke.createNode("Grade")         
    except:
        nuke.createNode("Grade")


