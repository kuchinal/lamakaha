def out():
  import nuke
  n=nuke.selectedNode()
  n['operation'].setValue('stencil')
  n['bbox'].setValue('union')
