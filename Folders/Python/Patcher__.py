import nuke
def Patcher():
    a = nuke.createNode("Patcher_")
    a['currentframe'].setValue(nuke.frame())
    a['cloneframe'].setValue(nuke.frame())

