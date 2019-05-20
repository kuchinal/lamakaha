def screen():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('screen')