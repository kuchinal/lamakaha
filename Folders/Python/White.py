def White():
    import nuke
    b = nuke.createNode("Shuffle")
    b['alpha'].setValue(6)
    b['tile_color'].setValue(4294967295)
    b['label'].setValue("White Alpha")   
