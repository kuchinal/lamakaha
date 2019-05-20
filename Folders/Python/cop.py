import nuke
def cop():
   n = nuke.selectedNode()
   a=n['to1'].getValue()
   b=n['to2'].getValue()
   c=n['to3'].getValue()
   d=n['to4'].getValue()
   n['from1'].setValue(a)
   n['from2'].setValue(b)
   n['from3'].setValue(c)
   n['from4'].setValue(d)
