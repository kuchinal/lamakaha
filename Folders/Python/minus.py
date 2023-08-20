def minus():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('minus')