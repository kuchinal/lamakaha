import nuke
def nodeInBackDropp(someNode,someBackDropp):
    inside = 0
    x = int(someNode['xpos'].value())
    y = int(someNode['ypos'].value())
    xb = int(someBackDropp['xpos'].value())
    xy = int(someBackDropp['ypos'].value())
    w = int(someBackDropp['bdwidth'].value())+xb
    h =int(someBackDropp['bdheight'].value())+xy
    if x>xb and x<w and y>xy and y<h:
        inside = 1
    return inside