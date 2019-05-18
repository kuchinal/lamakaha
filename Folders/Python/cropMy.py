import nuke
def cropMy():
    try: 
        if 'Deep' in nuke.selectedNode().Class() and "DeepHoldout" not in nuke.selectedNode()['name'].value() and "DeepToImage" not in nuke.selectedNode()['name'].value(): 
            nuke.createNode("DeepCrop")
        else:
            nuke.createNode("Crop")   
    except: 
        nuke.createNode("Crop")