import nuke
def constant():
  u = nuke.createNode("Constant")
  u['channels'].setValue("rgba")
  u['color'].setValue(1)