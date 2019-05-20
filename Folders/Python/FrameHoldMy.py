def FrameHoldMy():
 import nuke
 frame = nuke.tcl('frame')
 frame = int(frame)
 pause = nuke.createNode("FrameHold")
 pause['first_frame'].setValue(frame)