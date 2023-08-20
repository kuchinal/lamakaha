#            elif xb<x and yb<y and xb>x-300 and yb>y-400 and ba['label'].value()== "File Out":################################################################## Fie out case
import nuke
import nukescripts
def fileOutRFW():

    n =  nuke.selectedNode()
    xo = int(n['xpos'].value())
    yo = int(n['ypos'].value())

    index = n['file'].value().find('_v')
    version =  n['file'].value()[index+1:index+6]
    n['label'].setValue(version)
    n.setSelected(True)

    ### moving old results down
    a = nuke.allNodes("Read")
    a.remove(n)
    for node in a:
        y = int(node['ypos'].value())
        x = int(node['xpos'].value())
        if x> xo-40 and x< xo+40 and y> yo:
            node.setXYpos(x,y+85)
            node.setSelected(False)
    nukescripts.connect_selected_to_viewer(4)
    


# n = nuke.selectedNode()
# v =  nuke.ViewerWindow.node(nuke.activeViewer())
# nukescripts.connect_selected_to_viewer(4)