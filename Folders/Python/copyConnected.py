import nuke
import nukescripts

def copyConnected():    
    ### group the selected nodes
    selNodes = nuke.selectedNodes()

    ### we start the per node loop
    for node in selNodes:
        
        ### original list with dependencies to check if the node is connected
        dep = node.dependencies(nuke.INPUTS | nuke.HIDDEN_INPUTS)
        
        ### condition if the list is not empty (unconnected node)
        if dep:

            ### creates empty dict where we will add our inputs and connected nodes
            depDict = {}

            ## we get the number of inputs connected and we create a list with the range
            inputMax = node.inputs()
            inputRange = range(0,inputMax)

            ### we loop per input and store the name of the node connected to it (the if statement is in case there connection is empty it will do nothing)
            for inputCon in inputRange:
                inputNode = node.input(inputCon)
                if inputNode:
                    nodename = inputNode['name'].value()
                    depDict[inputCon] = nodename
        
            ### we check if our node selected is a wired or anchor node (trixter only)
            if node.knob('connection'):
                connection = node.knob('connection').getValue()

            ### we create the temp knobs with the dictionary of inputs and nodes (if the node is connected of course)
            else:
                tempTab = nuke.Tab_Knob('temp_tab', 'temp tab')
                node.addKnob(tempTab)
                depDictStr = str(depDict)
                tempText = nuke.Text_Knob('connectionTemp', 'connected to: ' , depDictStr)
                node.addKnob(tempText)

    

    ### copy paste the nodes
    nukescripts.node_copypaste()


    ### group the new nodes created that are selected by default
    newNodes = nuke.selectedNodes()

    ### start of the loop for the new nodes
    for node in newNodes:

        ### we check if our node selected is a wired or anchor node (trixter only) and connects it to its input if the input is not duplicated
        if node.knob('connection'):
            anchor = node['connection'].value()
            inputNode = nuke.toNode(anchor)
            if inputNode not in selNodes:
                node.setInput(0,inputNode)

        ### we retrieve the dict knob and set it as dictionary
        elif node.knob('connectionTemp'):
            anchorStr = node['connectionTemp'].value()
            anchorDict = eval(anchorStr)

            ### for every key we retrieve the value of the dict
            for key in anchorDict:
                element = anchorDict[key]
                ### important fuck up, i don't know why nuke does not like the string resultant so i force the evaluation
                #evalInput = eval(element)

                ### we connect to the original input if it is not copied (selNodes) using the key (input number) and the value (node)
                inputNode = nuke.toNode(element)
                if inputNode not in selNodes:
                    node.setInput(key,inputNode)
            
            ### deletes the temp knobs from new nodes
            knobs = node.knobs()
            node.removeKnob(knobs['connectionTemp'])
            node.removeKnob(knobs['temp_tab'])

        ### we delete the variable count so it does'nt pile up
        # if 'count' in locals():
        #     del count     


    ### deletes the temp knobs from old selected nodes
    for node in selNodes:
        if node.knob('connectionTemp'):
            node.hideControlPanel()
            allknobs = node.knobs()
            node.removeKnob(allknobs['connectionTemp'])
            node.removeKnob(allknobs['temp_tab'])

       
