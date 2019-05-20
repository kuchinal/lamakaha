import nuke
def expressionMy():
    try: 
        if 'Deep' in nuke.selectedNode().Class() and "DeepHoldout" not in nuke.selectedNode()['name'].value() and "DeepToImage" not in nuke.selectedNode()['name'].value(): 
            nuke.createNode("DeepExpression")
        else:
            nuke.createNode("Expression")   
    except: 
        nuke.createNode("Expression")