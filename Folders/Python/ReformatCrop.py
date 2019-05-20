def ReformatCrop():
    import nuke
    r = nuke.createNode("Reformat")
    r['resize'].setValue('none')
    r['center'].setValue(0)
    r['pbb'].setValue(1)
