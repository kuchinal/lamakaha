import nuke
	



def disabler():
    u = nuke.allNodes("IDistort")
    for i in u:
      i['disable'].setValue(1)
    u = nuke.allNodes("VectorBlur")
    for i in u:
      i['disable'].setValue(1)
    u = nuke.allNodes("ZBlur")
    for i in u:
      i['disable'].setValue(1)
    u = nuke.allNodes("LightWrap")
    for i in u:
      i['disable'].setValue(1)   

