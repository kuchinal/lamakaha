def Pixo3DBuild():
    import nuke
    import pixo3D
    import PixoConnect
    
    panel = nuke.Panel("Card to track")
    panel.addBooleanCheckBox('Autolabel', False)
    panel.addBooleanCheckBox('Create Tree', True)
    panel.addBooleanCheckBox('Connect', False)
    if panel.show():
        n = nuke.selectedNodes()
        Labell = panel.value("Autolabel")
        Tree = panel.value("Create Tree")
        Connect = panel.value("Connect")
    
    if Labell is True:
        pixo3D.pixo3D()
    if Tree is True:
        nuke.nodePaste('H:/.nuke/GeneralSetups/VrayTemplate.nk')
        #t = nuke.selectedNodes()
    if Connect is True:
        for i in n:
            i.setSelected(True)
            #nuke.setSelected(t)
        PixoConnect.PixoConnect()
    for i in n:
        i.setSelected(False)




