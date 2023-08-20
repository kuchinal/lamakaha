
import nuke

def Inverter():
  n = nuke.selectedNode()
  name = n['name'].value()
  t = n['translate'].value()
  r= n['rotate'].value()
  tOrder = n['xform_order'].value()
  rOrder = n['rot_order'].value()
  new = nuke.createNode('Axis')
  new['translate'].setValue([-1*t[0],-1*t[1],-1*t[2]])
  new['rotate'].setValue([-1*r[0],-1*r[1],-1*r[2]])
  new['xform_order'].setValue(tOrder[::-1])
  new['rot_order'].setValue(rOrder[::-1])
  new['name'].setValue('Inverter'+name)
  new['label'].setValue(str(nuke.frame()))
  new['tile_color'].setValue(1)
