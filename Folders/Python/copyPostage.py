def copyPostage():
    import nuke
    import nukescripts
    ###collecting data about connections
    g= nuke.selectedNodes()
    for n in g:
        if n.Class() == "PostageStamp" and n['hide_input'].value() == 1 or n.Class() == "Shuffle" and n['hide_input'].value() == 1 or n.Class() == "NoOp" and n['hide_input'].value() == 1:
            n['hide_input'].setValue(0)
            dep = n.dependencies(nuke.INPUTS)[0]
            n['hide_input'].setValue(1)
            lab = n['help'].setValue(dep['name'].value())
    
    ### standart copy paste
    count = 0
    for rr in g:
        count = count +1
        x = int(rr['xpos'].value())
        y = int(rr['ypos'].value())
    nukescripts.node_copypaste()
    if count ==1:
        nuke.selectedNode().setXYpos(int(x-100),int(y+50))
    
    ####reconnecting postages
    e= nuke.selectedNodes()
    for n in e:
        if n.Class() == "PostageStamp" and n['hide_input'].value() == 1 or n.Class() == "Shuffle" and n['hide_input'].value() == 1 or n.Class() == "NoOp" and n['hide_input'].value() == 1 or n.Class() == "DeepExpression" and n['hide_input'].value() == 1:
            connect = nuke.toNode(n['help'].value())
            if connect not in g:
                n.setInput(0,connect) 
                n['hide_input'].setValue(1)
