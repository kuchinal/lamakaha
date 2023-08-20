def shuffleAlpha():
    import nuke
    import nukescripts
    import Axis_My
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(4)
                a['green'].setValue(4)
                a['blue'].setValue(4)
                a['alpha'].setValue(4) 
            else:
                Axis_My.Axis_My() 
        else:
            Axis_My.Axis_My()           
    except:
        Axis_My.Axis_My()


