import nuke



def create_node():
  q = nuke.nodes.NoOp()
  q.setName('Runner')
  text2 = nuke.Text_Knob("Please rename  your Parent Node to    MAMA ")
  text3 = nuke.Text_Knob("Please select  all the children nodes and after that push Run ")
  
  position = nuke.XYZ_Knob("PositionOffset","Position Time Offset")
  position.setTooltip('This will offset a position of your children by xyz ')
  
  rotation = nuke.XYZ_Knob("RotationOffset","Rotation Time Offset")
  rotation.setTooltip('This will offset a rotation of your children by xyz ')
  
  FrameRange = nuke.WH_Knob("FrameRange","FrameRange",)
  FrameRange.setTooltip('Frame Range for calculation')
  FrameRange.setRange(0,500)
  
  text = nuke.Text_Knob("If you ready push run!!!")
  run = nuke.PyScript_Knob("Run")
  
  u = 'delayer_son.TimeDelay()'
  run.setValue(u)
  q.addKnob(text2)
  q.addKnob(position)
  q.addKnob(rotation)
  q.addKnob(FrameRange)
  q.addKnob(text3)
  q.addKnob(run)
  
  