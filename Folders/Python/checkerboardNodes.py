def checkerboardNodes(mode='y'):
    import nuke
    count=0
    moveBy=75

    for i in nuke.selectedNodes():
        m=count%3
        
        if mode=='y':
            i.autoplace()
            i.setXYpos(i.xpos(), i.ypos()+(m*moveBy))
        elif mode =='x': 
            i.autoplace()
            i.setXYpos(i.xpos()+(m*moveBy), i.ypos())

        count+=1