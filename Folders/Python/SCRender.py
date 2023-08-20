def SCRender():
  import nuke
  nuke.createNode("ScanlineRender")
  nuke.createNode("Remove")
  