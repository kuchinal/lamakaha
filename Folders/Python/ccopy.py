def ccopy():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('copy')
