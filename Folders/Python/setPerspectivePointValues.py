def setPerspectivePointValues():
    import nuke
    w = int (nuke.root().knob('format').value().width())
    h = int (nuke.root().knob('format').value().height())
    wHalf = int (w/2)
    hHalf = int (h/2)

    persp = nuke.thisNode()
    persp[ 'origin' ].setValue( [wHalf, hHalf] )
    persp[ 'point1' ].setValue( [0, h] )
    persp[ 'point2' ].setValue( [wHalf+1, h] )
    persp[ 'point3' ].setValue( [w, h] )
    persp[ 'point4' ].setValue( [0, hHalf+1] )
    persp[ 'point5' ].setValue( [w, hHalf+1] )
    persp[ 'point6' ].setValue( [0, 0] )
    persp[ 'point7' ].setValue( [wHalf+1, 0] )
    persp[ 'point8' ].setValue( [w, 0] )