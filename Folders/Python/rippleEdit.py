import nuke 
def toggleRippleEdit(): 
    try: 
        theSelectedNode = nuke.selectedNode()  
    except: 
        try: 
            for aNode in nuke.allNodes(): 
                if aNode.shown(): 
                    theSelectedNode = aNode 
        except: 
            pass 
    basicProccess = nuke.activeViewer().node()['viewerProcess'].value()
    if basicProccess != "RippleEdit":
        currentLUT = nuke.activeViewer().node()['viewerProcess'].value()
        nuke.activeViewer().node()['label'].setValue(currentLUT)


    if theSelectedNode['toolbar_ripple'].value() == False: 
        theSelectedNode['toolbar_ripple'].setValue(True) 
        theViewer = nuke.activeViewer().node() 
        theViewer['viewerProcess'].setValue("RippleEdit") 
    
    elif theSelectedNode['toolbar_ripple'].value() ==True: 
        theSelectedNode['toolbar_ripple'].setValue(False) 
        theViewer = nuke.activeViewer().node()
        oldViewer = nuke.activeViewer().node()['label'].value() 
        theViewer['viewerProcess'].setValue(oldViewer) 
if __name__ == '__main__': 
   toggleRippleEdit() 
