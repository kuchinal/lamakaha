import nuke

def Dots():
    dotList,dotListX= [],[]
    Dsize = int(nuke.toNode("preferences")['dot_node_scale'].value()*12)
    nodes = nuke.selectedNodes()
    count = 0
    same = 1
    old = ""
    for selected in nodes:
        selectedX = selected.xpos()
        selectedY = selected.ypos()
        selectedW = selected.screenWidth()
        selectedH = selected.screenHeight()



        # checking inputs and assigning variables
        try:# check if input 0 is exist
            A = selected.input(0)
            AX = A.xpos()
            AY = A.ypos()
            AW = A.screenWidth()
            AH = A.screenHeight()
            AClass = A.Class()
            if count == 0:
                old = A
                count = count+1
            else:
                if old != A:
                    same = 0



        except:
            AX = selected.xpos()
            AY = selected.ypos()
            AW = selected.screenWidth()
            AH = selected.screenHeight()
            AClass = "no classs"
        try:# check if input 1 is exist
            B = selected.input(1)
            BX = B.xpos()
            BY = B.ypos()
            BW = B.screenWidth()
            BH = B.screenHeight()
            BClass = B.Class()
            print " Input 1 found   " + B['name'].value()
        except:
            BX = selected.xpos()
            BY = selected.ypos()
            BW = selected.screenWidth()
            BH = selected.screenHeight()
            BClass = "no classs"
            print " no input1 found        "
        try:# check if input 2 is exist
            C = selected.input(2)
            CX = C.xpos()
            CY = C.ypos()
            CW = C.screenWidth()
            CH = C.screenHeight()
            CClass = C.Class()
            print " Input 2 found   " + C['name'].value()
        except:
            print " "



        # setting position
        if B and not C:#two inputs found
            Dot = nuke.nodes.Dot()
            
            if BX == selectedX or BX-34 == selectedX:# above node case
                print 'above node case'
                t = nuke.selectedNode()
                depB = t.dependencies(nuke.INPUTS)[0]

                try:
                    depA = t.dependencies(nuke.INPUTS)[1]
                except:
                    depA = t.dependencies(nuke.INPUTS)[0]

                depA.setSelected(True)
                x2 = depA.xpos()
                y2 = depA.ypos()
                w,h = depA.screenWidth(),depA.screenHeight()


                dot = nuke.nodes.Dot()
                dot.setXYpos(selectedX-200,selectedY+selectedH/2-Dsize/2)
                dot2 = nuke.nodes.Dot()
                if BX-34 == selectedX:
                    dot2.setXYpos(selectedX-200,y2)
                else:
                    dot2.setXYpos(selectedX-200,y2+h/2-Dsize/2)
                dot2.setInput(0,depA)
                dot.setInput(0,dot2)
                t.setInput(1,dot)
                nuke.delete(Dot)
            else:#normal merge case
                Dot.setInput(0,B)
                selected.setInput(1,Dot)
                Dot.setXYpos(BX+BW/2-Dsize/2,selectedY+selectedH/2-Dsize/2)

            if A.Class()== "Dot":
                selected.knob("xpos").setValue(AX-selectedW/2+Dsize/2)
            else:        
                selected.knob("xpos").setValue(AX)


            print 'two inputs found'
        
        elif C:#three inputs found
             
            if "Scanline" in selected.Class():
                if BClass == "no classs":
                    pass
                else:
                    if B.Class()== "Dot":
                        selected.setXYpos(BX-selectedW/2+Dsize/2,selectedY)
                    else:
                        selected.setXYpos(BX,selectedY)

                dot = nuke.nodes.Dot(xpos=CX+CW/2-Dsize/2, ypos=selectedY+selectedH/2-Dsize/2)
                dot.setInput(0,C)
                selected.setInput(2,dot)

                if AClass == "no classs":
                    pass
                else:
                    dot = nuke.nodes.Dot(xpos=AX+AW/2-Dsize/2, ypos=selectedY+selectedH/2-Dsize/2)
                    dot.setInput(0,A)
                    selected.setInput(0,dot)
                print "Scanline"
            if "Merge" in selected.Class() or "Roto" in selected.Class()or "Keymix" in selected.Class():

                if A.Class()== "Dot":
                    selected.knob("xpos").setValue(AX-selectedW/2+Dsize/2)
                else:        
                    selected.knob("xpos").setValue(AX)

                dot = nuke.nodes.Dot(xpos=CX+CW/2-Dsize/2, ypos=selectedY+selectedH/2-Dsize/2)
                dot.setInput(0,C)
                selected.setInput(2,dot)

                dot = nuke.nodes.Dot(xpos=BX+BW/2-Dsize/2, ypos=selectedY+selectedH/2-Dsize/2)
                dot.setInput(0,B)
                selected.setInput(1,dot)


                print 'three input found'

        else:#one input found
            print 'one input found'
            Dot = nuke.nodes.Dot() 
            Dot.setInput(0,A)
            selected.setInput(0,Dot)        
            Dot.setXYpos(selectedX+selectedW/2-Dsize/2,AY+AH/2-Dsize/2) 
            dotList.append(Dot)
            dotListX.append(Dot.xpos())


    # if len(dotList)>1 and same == 1:
    #     dotListX.sort()
    #     if A.xpos()>dotListX[0]:
    #         dotListX.reverse()
    #     d=A
    #     for one in dotListX:
    #         for sec in dotList:
    #             if sec.xpos() == one:
    #                 sec.setSelected(True)
    #                 r = nuke.createNode("Dot")
    #                 r.setSelected(False)
    #                 sec.setSelected(False)
    #                 sec.setInput(0,d)
    #                 d=sec




    ###################################################

