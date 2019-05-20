import nuke
def Input():
     s = nuke.selectedNodes()
     for s in s:
         cur = s['hide_input'].getValue()
         if cur == 0:
            s['hide_input'].setValue(1)
         else:
            s['hide_input'].setValue(0)