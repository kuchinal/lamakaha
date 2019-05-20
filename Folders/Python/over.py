def over():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('over')
  n['bbox'].setValue('union')