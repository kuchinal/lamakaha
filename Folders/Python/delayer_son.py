import nuke
	



def TimeDelay ():
    e = nuke.toNode('Runner')
    incr_x = e['PositionOffset'].getValue(0)
    incr_y = e['PositionOffset'].getValue(1)
    incr_z = e['PositionOffset'].getValue(2)
    incr_xr = e['RotationOffset'].getValue(0)
    incr_yr = e['RotationOffset'].getValue(1)
    incr_zr = e['RotationOffset'].getValue(2)
    range = e['FrameRange'].getValue()
    a = nuke.toNode('MAMA')
    b = nuke.selectedNodes()
    d = 0
    k = 0
    m = 0
    dr = 0
    kr = 0
    mr = 0
    for g in b:
           f = 0
           d = d - incr_x
           k = k - incr_y
           m = m - incr_z
           s = d
           n = k
           r = m
           dr = dr - incr_xr
           kr = k - incr_yr
           mr = mr - incr_zr
           sr = dr
           nr = kr
           rr = mr
           while f < range:
               x = a['translate'].getValueAt(s,0)
               y = a['translate'].getValueAt(n,1)
               z = a['translate'].getValueAt(r,2)
               xr = a['rotate'].getValueAt(sr,0)
               yr = a['rotate'].getValueAt(nr,1)
               zr = a['rotate'].getValueAt(rr,2)
               g['translate'].setValueAt(x,f,0)
               g['translate'].setValueAt(y,f,1)
               g['translate'].setValueAt(z,f,2)
               g['rotate'].setValueAt(xr,f,0)
               g['rotate'].setValueAt(yr,f,1)
               g['rotate'].setValueAt(zr,f,2)
               g['translate'].setKeyAt(f)
               g['rotate'].setKeyAt(f)                    
               f = f + 1
               s = s + 1
               n = n + 1
               r = r + 1
               sr = sr + 1
               nr = nr + 1
               rr = rr + 1