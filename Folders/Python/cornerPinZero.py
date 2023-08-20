def cornerPinZero():
    import nuke
    n = nuke.thisNode()
    frame = nuke.frame()
    n['label'].setValue("Ref frame " + str(frame))
    for one in range (1,5):
        one = str(one)
        v = n['to'+one].value()
        n["from"+one].setValue(v)   
        n["from"+one].clearAnimated()