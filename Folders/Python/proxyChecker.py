import nuke
import shutil
def proxyChecker():
    nodes = nuke.allNodes("Read")
    for node in nodes:  
        proxy = node['proxy'].getValue()
        file = node['file'].getValue()
        name = file.rpartition("/")[2]
        if not "workspace" in file:
            if not "workspace" in proxy:
                nuke.message(name + "  have no proxy")