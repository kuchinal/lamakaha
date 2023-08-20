import nuke
def IBKMy():
	nuke.nodePaste(UserDir+"/GeneralSetups/IBK.nk")
	a = nuke.selectedNode()
	print a
	nuke.show(a)