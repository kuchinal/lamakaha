def fademult():
    import nuke
    n = nuke.createNode("Multiply")
    n['channels'].setValue("rgba")
