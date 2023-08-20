def ColorspaceMy():
    import nuke
    try:
        n= nuke.selectedNode()
        dep = n.dependencies(nuke.INPUTS)[0]
        x = n.xpos()
        y = n.ypos()
        first = nuke.nodes.Colorspace()
        first.setXYpos(x,y-50)
        first.setInput(0,dep)
        name = first['name'].value()
        string = name + ".colorspace_out"
        second = nuke.nodes.Colorspace()
        second.setXYpos(x,y+50)
        second.setInput(0,n)
        second["colorspace_in"].setExpression(string)
        n.setInput(0,first)
    except:
        nuke.createNode("Colorspace")
