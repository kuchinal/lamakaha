def myReformat():
    import nuke 
    try: 
        if "deep" in str(nuke.selectedNode().metadata()) and "depth" not in str(nuke.selectedNode().channels()): 
            return nuke.createNode( "DeepReformat")
        else: 
            raise ValueError 
    except: 
        return nuke.createNode("Reformat" ) 
        
