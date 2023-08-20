def removeLocalCache():
    import shutil
    import nuke
    n = nuke.selectedNode()
    file = n['file'].value()
    local = nuke.toNode('preferences').knob("localCachePath").value()
    path = local+"/"+file.rpartition("/")[0]+"/"
    path = path.replace('Y:', 'Y_')
    shutil.rmtree(path)