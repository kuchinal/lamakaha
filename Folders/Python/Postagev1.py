import nuke
def Postage():
  t= nuke.selectedNodes()
  for t in t:
      label = t['label'].value()
      x = t.xpos()
      y = t.ypos()
      y = int(y)
      y = y+100
      u = nuke.nodes.PostageStamp(postage_stamp = 0, note_font_size =   20, tile_color = 4000,name = label, hide_input = 1 )
      W = nuke.selectedNodes("Read")
      if t.Class() == "Read":
        first = t['first'].value()
        last = t['last'].value()
        frames = last - first
        frames = str(frames) 
        first = str(first)
        last = str(last)
        newlab = first+"-"+last+"("+frames+")"
        u['label'].setValue(newlab)
      u.setInput(0,t)
      print x
      print y
      u.setXYpos(x,y)
