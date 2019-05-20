
import nuke

def SmartOffset():
  r =nuke.Root().knob('first_frame').getValue()
  n = nuke.selectedNode()
  o=n.Class() 
  if o == "Read":
    t = n['first'].getValue()
    u = n['last'].getValue()
    b = u - t
    b = int(b)
    shot = str(b)
    y=nuke.createNode("TimeOffset")
    y['time_offset'].setValue(-t+r)
    n['postage_stamp'].setValue(0)
    y['postage_stamp'].setValue(0)
    n['label'].setValue(shot + " frames")
    y['label'].setValue(shot + " frames")
  else:
    nuke.createNode("TimeOffset")
    
    
    

def SmartOffset7():
  r =nuke.Root().knob('first_frame').getValue()
  n = nuke.selectedNode()
  o=n.Class() 
  if o == "Read":
    t = n['first'].getValue()
    u = n['last'].getValue()
    b = u - t
    b = int(b)
    shot = str(b)
    y=nuke.createNode("TimeClip")
    y['frame_mode'].setValue("offset")
    y['frame'].setValue(str(t-r))
    n['postage_stamp'].setValue(0)
    y['postage_stamp'].setValue(0)
    n['label'].setValue(shot + " frames")
    y['label'].setValue(shot + " frames")
  else:
    nuke.createNode("TimeClip")
