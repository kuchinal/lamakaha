import nuke

def bezierTracked():
    try:
        tracker = nuke.selectedNode()
        if tracker.Class()=="Tracker3":
            x = tracker['xpos'].value()
            y = tracker['ypos'].value()
            label = tracker['label'].value()
            bezier = nuke.nodes.Bezier()
            bezier.setXYpos(x,y+100)
            bezier['label'].setValue(label)
            #bezier['hide_input'].setValue(1)
            try:   
                bezier['translate'].copyAnimation(0,tracker['translate'].animation(0))
                bezier['translate'].copyAnimation(1,tracker['translate'].animation(1))
            except:
                print "no translate"
    
            try:    
                bezier['rotate'].copyAnimation(0,tracker['rotate'].animation(0))
            except:
                print "no rotate"
            
            try:
                bezier['scale'].copyAnimation(0,tracker['scale'].animation(0))
                bezier['scale'].copyAnimation(1,tracker['scale'].animation(1))
            except:
                print "no scale"
            try:
                bezier['skew'].copyAnimation(0,tracker['skew'].animation(0))
                bezier['skew'].copyAnimation(1,tracker['skew'].animation(1))
            except:
                print "no skew"
            try:
                bezier['center'].copyAnimation(0,tracker['center'].animation(0))
                bezier['center'].copyAnimation(1,tracker['center'].animation(1))
            except:
                print "no center"
        else:
                 nuke.createNode("Bezier")
    except:
        nuke.createNode("Bezier")