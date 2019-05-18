def Black():
    import nuke
    b = nuke.createNode("Shuffle")
    b['alpha'].setValue(5)
    b['tile_color'].setValue(1)
    b['label'].setValue("Black Alpha")   
    print "hallo"
