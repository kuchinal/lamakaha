def pixo3D():
    import nuke

    n = nuke.selectedNodes()
    for node in n:
        file = node['file'].value()
        name = file.rsplit('.')[1]
        node['label'].setValue(name)
    t= nuke.selectedNodes()
    for p in n:
        p['autolabel'].setValue("nuke.thisNode().name() + \"\\n\" + nuke.thisNode()['label'].value()")
        p['note_font_size'].setValue(20)
