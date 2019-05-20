def preferencesOverride():
    import nuke
    #nuke.toNode('preferences')['diskCacheGB'].setValue(25)
    nuke.toNode('preferences')['maxPanels'].setValue(1)
    nuke.toNode('preferences')['UIAnimatedColor'].setValue(0x88e0eff)
    nuke.toNode('preferences')['ArrowColorElbow'].setValue(0xffff0000)
    nuke.toNode('preferences')['ArrowColorLeft'].setValue(0x4f0000ff)
    nuke.toNode('preferences')['ArrowColorRight'].setValue(0)
    nuke.toNode('preferences')['ArrowColorUp'].setValue(0x540000ff)
    nuke.toNode('preferences')['InputArrowSize'].setValue(18)
    nuke.toNode('preferences')['LeftInputArrowSize'].setValue(10)
    nuke.toNode('preferences')['OutputArrowSize'].setValue(10)
    nuke.toNode('preferences')['ArrowheadLength'].setValue(10)
    nuke.toNode('preferences')['ArrowheadWidth'].setValue(10)
    nuke.toNode('preferences')['ArrowWidth'].setValue(4)
    nuke.toNode('preferences')['AlreadyQueuedItemColor'].setValue(0x4f0000ff)    
    nuke.knobDefault( 'preferences.AlreadyQueuedItemColor', '0x4f0000ff')
    
    nMajor = nuke.NUKE_VERSION_MAJOR 
    if nMajor >6: 
        nuke.toNode('preferences')['goofy_foot'].setValue(0)
        nuke.toNode('preferences')['viewer_handle_pick_size'].setValue(15)
        #nuke.toNode('preferences')['DfltBezAutokey'].setValue(0)
        nuke.toNode('preferences')['UIRotoPointColor'].setValue(0xff0000ff)
        nuke.toNode('preferences')['UIRotoCurveColor'].setValue(0xffff00ff)
        nuke.toNode('preferences')['UIRotoTransformJackColor'].setValue(0xbc00ff)
        nuke.toNode('preferences')['UICacheframeColor'].setValue(0xffff00ff)
        #nuke.toNode('preferences')['UIRotoLockedColor'].setValue(0xcccccfff)
        nuke.toNode('preferences')['UISplineWarperSrcStippled'].setValue(0)
        nuke.toNode('preferences')['UISplineWarperDstStippled'].setValue(0)
        nuke.toNode('preferences')['UISplineWarperASourceColor'].setValue(0xffff00ff)
        nuke.toNode('preferences')['UISplineWarperBSourceColor'].setValue(0xffffff)
        nuke.toNode('preferences')['UISplineWarperADestColor'].setValue(0x606000ff)
        nuke.toNode('preferences')['UISplineWarperBDestColor'].setValue(0x4259ff)
        nuke.toNode('preferences')['UISplineWarperCorrespondenceColor'].setValue(1)
        nuke.toNode('preferences')['UISplineWarperDstStippled'].setValue(0xff8400ff)
        nuke.toNode('preferences')['UISplineWarperBoundaryColor'].setValue(0xffffffff)


