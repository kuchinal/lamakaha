def plus():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('plus')