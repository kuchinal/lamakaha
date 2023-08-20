
import nuke


def NetRender():
 temp = nuke.scriptSave()
 n = nuke.allNodes('Read')
 for node in n:
    path = node['file'].getValue()
    new = path[3:]
    newpath = '//work/stripe (s)/' + new
    node = node['file'].setValue(newpath)
 n = nuke.allNodes('Write')
 for node in n:
   path = node['file'].getValue()
   new = path[3:]
   newpath = '//work/stripe (s)/' + new
   node = node['file'].setValue(newpath)
 h = nuke.scriptSave('//Farm/mfarm/FarmRender/Render.nk')
 h = nuke.scriptSave('//Farm2/D/Farm2Render/Render.nk')
 j = nuke.undo()
