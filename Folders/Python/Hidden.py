import nuke
def Hidden():
    n = nuke.selectedNode()['name'].value()
    all = nuke.allNodes()
    for node in all:
        try:
            t = node['connection'].value()
            if t == n:
                node.setSelected(True)
        except:
            pass
         