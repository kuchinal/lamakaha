def flash():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
      lastFrame=nuke.root().knob('last_frame').value()+1
      frame = 1001
      while frame<lastFrame:
        flashing = n['scaling'].getValueAt(frame,0)
        if flashing>0:
            posix = n['translate'].getValueAt(frame,0)
            posiy = n['translate'].getValueAt(frame,1)
            posiz = n['translate'].getValueAt(frame,2)
            fade = nuke.nodes.Multiply()
            fadeposx = fade['xpos'].value()
            fadeposy = fade['ypos'].value()
            card = nuke.nodes.Card2()
            card['xpos'].setValue(fadeposx)
            card['ypos'].setValue(fadeposy-50)
            card.setInput(0,fade)
            card['translate'].setValueAt(posix,frame,0)
            card['translate'].setValueAt(posiy,frame,1)
            card['translate'].setValueAt(posiz,frame,2)
            card['uniform_scale'].setValue(1000)
            exp = "frame<"+str(frame)+"?0:1"
            fade['value'].setExpression(exp)
            TO = nuke.nodes.TimeOffset()
            TO['time_offset'].setValue(frame)
            fade.setInput(0,TO)
        frame = frame+1
