def Axis_My():  
    import nuke
    nuke.nodePaste('H:/.nuke/GeneralSetups/AxisMy.nk')
    n = nuke.selectedNode()
    nuke.show(n)


