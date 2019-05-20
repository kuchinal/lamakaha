def under():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('under')
  n['bbox'].setValue('union')