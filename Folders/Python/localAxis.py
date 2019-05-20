def createLocalAxis(sn=nuke.selectedNodes()):
    #set back to root to stop Nuke working inside the wrong node
    nuke.root().begin()

    nodeList=[]
    if not sn:
        nuke.message('please select some Geo/Camera nodes')
        return

    else:

        for i in sn:
            
            if 'snap_menu' in i.knobs():
                nodeList.append(i.name())
        if not nodeList:                
                nuke.message('No Geo/Camera nodes selected')
                return
    print nodeList

    # to do create the nodes from the above list and set up the local axis

    for n in nodeList[::-1]:
        node=nuke.toNode(n)
        if 'Camera' in node.Class():
            zeroPosNode='Axis'
            isCam=True
        else:
            zeroPosNode='TransformGeo'
            isCam=False
        x_ord=node['xform_order'].value()
        r_ord=node['rot_order'].value()
        #print x_ord[::-1], r_ord[::-1]    


        #create Group
        #NOTE need to deselect everything as it will copy the selection into the group
        nuke.selectAll()
        nuke.invertSelection()

        g=nuke.makeGroup(False) # False stops it opening the group. 
        g.setName('localAxis')

        #work inside the group
        g.begin()
        # Do stuff inside your group, e.g. nuke.nodes.MyNode()
        zeroPos=nuke.createNode(zeroPosNode, inpanel=False)
        zeroPos.setName('ZeroPosition')
        putBack=nuke.createNode('Axis2', inpanel=False)
        putBack.setName('positionGeoBack')
        localAx=nuke.createNode('Axis2', inpanel=False)
        localAx.setName('LocalAxis')

        # hook them up
        # gets internally created nodes

        nInput=nuke.toNode('Input1')
        output=nuke.toNode('Output1')

        if isCam:
            #remove inputs first then reconnect
            zeroPos.connectInput(0,None)
            zeroPos.connectInput(0,None)
            localAx.connectInput(0,None)
            putBack.connectInput(0,None)
            zeroPos.connectInput(0,localAx)
            localAx.connectInput(0,putBack)
            output.connectInput(0,zeroPos)
            putBack.connectInput(0,nInput)
        else:
            g.connectInput(0,node)
            nInput=nuke.toNode('Input1')
            zeroPos.connectInput(0,nInput)
            zeroPos.connectInput(1,localAx)
            output.connectInput(0,zeroPos)


        ## offset positions
        g.autoplace()
        if isCam:
            putBack.setXYpos(int(nInput.xpos()+10), int(nInput.xpos()+100))
            localAx.setXYpos(int(putBack.xpos()), int(putBack.ypos()+100))
            zeroPos.setXYpos(int(localAx.xpos()), int(localAx.ypos()+100))
            output.setXYpos(int(nInput.xpos()), int(zeroPos.ypos()+100))

        else:
            zeroPos.setXYpos(int(nInput.xpos()), int(nInput.xpos()+150))
            localAx.setXYpos(int(zeroPos.xpos()-150), int(zeroPos.ypos()-18))
            putBack.setXYpos(int(localAx.xpos()), int(zeroPos.ypos()-150))


        ## link knobs to local axis
        knobsList=[('display','display'),('xform_order','transform order'),('rot_order','rotation order'),('translate','translate'),('rotate','rotate'),('scaling','scale'),('uniform_scale','uniform scale'),('skew','skew'),('pivot','pivot'),('useMatrix','specify matrix'),('matrix','local matrix')]

        for kn in knobsList: 
            knobName='%s.'+kn[0]
            link=nuke.Link_Knob(kn[0], kn[1])
            link.setLink(knobName % localAx.fullName())
            g.addKnob(link)

        ## set local axis parameters
        zeroPos['xform_order'].setValue(x_ord[::-1])     # reverse slice (start, end, step -1)
        zeroPos['rot_order'].setValue(r_ord[::-1])          
        zeroPos['translate'].setExpression('-'+n+'.translate')
        zeroPos['rotate'].setExpression('-'+n+'.rotate')
        zeroPos['scaling'].setExpression('1/'+n+'.scaling')
        zeroPos['uniform_scale'].setExpression('1/'+n+'.uniform_scale')
        zeroPos['pivot'].setExpression(n+'.pivot')
        putBack['xform_order'].setValue(x_ord)
        putBack['rot_order'].setValue(r_ord)
        putBack['translate'].setExpression(n+'.translate')
        putBack['rotate'].setExpression(n+'.rotate')
        putBack['scaling'].setExpression(n+'.scaling')
        putBack['uniform_scale'].setExpression(n+'.uniform_scale')
        putBack['pivot'].setExpression(n+'.pivot')
        # come out of the group
        g.end()

        if isCam:
            node.connectInput(0,g)
            





'''
reversing string an
sn=nuke.selectedNodes()
for n in sn:
    x_ord=n['xform_order'].value()
    r_ord=n['rot_order'].value()
    x_ord[::-1], r_ord[::-1]


    
example from Ivan on how to create the top group links to localAxis inside

link = nuke.Link_Knob('test', 'test')
link.setLink('%s.<knobname>' % <node_object>.fullName())
groupnode.addKnob(link)

'''

