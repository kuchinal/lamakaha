def Basic():
   import nuke		
   S = nuke.selectedNode()
   y = nuke.toNode("Basic")
   S.setInput(0,y)
