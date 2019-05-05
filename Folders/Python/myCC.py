def myCC():
    import nuke 
    try: 
        if nuke.selectedNode().channels() == []: 
            return nuke.createNode( "DeepColorCorrect2")
        else: 
            raise ValueError 
    except: 
        return nuke.createNode("ColorCorrect" ) 