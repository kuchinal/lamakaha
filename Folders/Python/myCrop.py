def myCrop():
    import nuke 
    try: 
        if "deep" in str(nuke.selectedNode().metadata()) and "depth" not in str(nuke.selectedNode().channels()): 
            return nuke.createNode( "DeepCrop")
        else: 
            raise ValueError 
    except: 
        return nuke.createNode("Crop" ) 
