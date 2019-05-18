def getColor():
    import nuke
    node = nuke.selectedNode()
    color= str(node['tile_color'].value())
    nuke.message(color)