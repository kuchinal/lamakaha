import nuke
	



def enabler():
    u = nuke.allNodes("IDistort")
    for i in u:
      i['disable'].setValue(0)
    u = nuke.allNodes("VectorBlur")
    for i in u:
      i['disable'].setValue(0)
    u = nuke.allNodes("ZBlur")
    for i in u:
      i['disable'].setValue(0)
    u = nuke.allNodes("LightWrap")
    for i in u:
      i['disable'].setValue(0)   

