def Black():
    import nuke
    b = nuke.createNode("Shuffle")
    b['alpha'].setValue(5)
    b['tile_color'].setValue(1)
    b['label'].setValue("Black Alpha")   
    print "hallo"



def White():
    import nuke
    b = nuke.createNode("Shuffle")
    b['alpha'].setValue(6)
    b['tile_color'].setValue(4294967295)
    b['label'].setValue("White Alpha")  