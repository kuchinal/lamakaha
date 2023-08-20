import nuke


def nameSet(name):    #will set a name for selected nodes
    import nuke
    a = nuke.selectedNodes()
    number = 1
    for n in a:
        n.setName(name+str(number))
        number =+1




def connectSoldiers(first,last,name):   # will connect selected nodes to nodes with a certain name, first and last are nodes numbers. example of naming: soldier_1, soldier_2,....

    import random 
    from random import randint
    dudes = []
    t = nuke.allNodes()
    for node in t:
        if name in node['name'].value():
            dudes.append(node)
    a = nuke.selectedNodes()
    for n in a:
        n.setInput(0, nuke.toNode(name+"_"+str(randint(first,last))))



def snapSoldiers():   # will create and snap Axises to selected vertices
    import nukescripts
    for point in nukescripts.snap3d.selectedPoints(): 
        t = nuke.nodes.Axis() 
        t['translate'].setValue(point) 
         
        ########################## 
        lst = [] 
        for point in nukescripts.snap3d.selectedPoints(): 
            lst.append(point) 

        count =0 
        for node in nuke.selectedNodes(): 
            node['translate'].setValue(lst[count]) 
            count+=1 


def createCards():   #create and connect a card to selected transform3D nodes
    a = nuke.selectedNodes()
    for node in a:
        if "TransformGeo" in node.Class():
            c = nuke.nodes.Card()
            x = int(node['xpos'].value())
            y = int(node['ypos'].value())
            node.setInput(0,c)
            c.setXYpos(x,y-200)
