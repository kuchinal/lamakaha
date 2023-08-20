
def SmartOffsetMy():
    import nuke
    import SmartOffset
    try: 
        if 'file' in nuke.selectedNode().knobs(): 
          SmartOffset.SmartOffset()
        else:
          nuke.createNode( 'TimeOffset' )
    except: 
        return nuke.createNode( 'TimeOffset' )
        
        
        