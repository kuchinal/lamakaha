import nuke
def Postage():
  t= nuke.selectedNode()
  o = t['label'].value()
  x = t.xpos()
  y = t.ypos()
  u = nuke.nodes.PostageStamp(postage_stamp = 1, note_font_size = 20, tile_color = 4000,)
  name = u['name'].value()
  #p = name.replace('PostageStamp',o)
  #nuke.toNode(p)
  newname = u['label'].setValue(o)
  u['hide_input'].setValue(1)
  u.setInput(0,t)
  u.setXYpos(x,y+100)
 