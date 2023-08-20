def multiply():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('multiply')
  n['bbox'].setValue('union')