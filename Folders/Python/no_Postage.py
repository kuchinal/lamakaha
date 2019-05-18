import nuke
def stamp():
  n = nuke.allNodes('Read')
  for g in n:
          g['postage_stamp'].setValue(0)

