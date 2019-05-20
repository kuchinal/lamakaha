def shuffleRed():
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
                a['red'].setValue(1)
                a['green'].setValue(1)
                a['blue'].setValue(1)
                a['alpha'].setValue(1) 
            else:
                nukescripts.create_read() 
        else:
            nukescripts.create_read()         
    except:
        nukescripts.create_read()


