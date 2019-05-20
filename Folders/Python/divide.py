def divide():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('divide')
  n['bbox'].setValue('union')