###    nodeKiss.py
###    v1.0
###    Created on 21/11/10 (dd/mm/yy)
###    Last modified on 25/11/10 (dd/mm/yy)
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import nuke

def nodeKiss():
    
    '''
    Flame's node kiss for nuke.
    It kisses (connects) the selected node to the node
    underneath once the two intersect
    '''
    
    ### Exception 1:
    ### Classes in this list will be connected in the opposite direction when
    ### both nodes being connected belong to the same class and have 1 input
    excp1 = ['Axis', 'Axis2']
    
    ### Exception 2:
    ### Classes in this list will be treated as 2 input nodes with no mask
    ### Do not add classes that have a single input to this list
    excp2 = ['Merge2']
    
    try:
        sn = nuke.selectedNode()
        an = nuke.allNodes()
    except:
        return
        
    snxp = sn.xpos() # x position of the selected node
    snyp = sn.ypos() # y position of the selected node
    
    snax = range( snxp, snxp + sn.screenWidth() ) # x area of the selected node
    snay = range( snyp, snyp + sn.screenHeight() ) # y area of the selected node
    
    snmx = sn.maxInputs() # the maximum number of inputs
    snmn = sn.minInputs() # the number of default visible inputs
    snci = sn.inputs() # the number of connected inputs
    
    try: # Gets mask input info
        sn['maskChannelInput']
        mask = True # Has mask
        mask_input = snmn - 1 # Mask input number
    except:
        mask = False # Has no mask
    
    snin = [] # A list of the names of the connected nodes
    for i in range(snci): # builds the snin list
        try:
            nn = sn.input(i).name()
            snin.append(nn)
        except:
            continue
    
    for n in an:
        if n is not sn:
            nxp = n.xpos() # x position of the node underneath
            nyp = n.ypos() # y position of the node underneath
            nax = range( nxp, nxp + n.screenWidth() ) # x area of the node underneath
            nay = range( nyp, nyp + n.screenHeight() ) # y area of the node underneath
            
            kissx = list( set(snax).intersection(set(nax)) ) # x intersection between n and sn
            kissy = list( set(snay).intersection(set(nay)) ) # y intersection between n and sn
            
            if kissx and kissy: # If areas intersect
                if snmx == 0:
                    # I'll implement this when I'm not feeling so lazy
                    # It will basically sort of do what Exception 1 does
                    return
                    
                else:
                    if sn.Class() not in excp1 and sn.Class() not in excp2: # If node not part of a exception
                        if mask: #If has mask
                            if n.name() not in snin: # If underneath node not already connected
                                if snci == mask_input: # If input about to be connected is mask input
                                    if  snci+1 < snmx-1: # and is not the last input
                                        sn.setInput(snci+1, n) # connect the next one
                                    else: # and is the last input reconnect the previous one
                                        sn.setInput(snmx-2, n)
                                else: # If input about to be connected is not a mask
                                    if snci < snmx: # and is within the number of available inputs
                                        sn.setInput(snci, n) # connect it
                                    else: # do nothing
                                        continue
                            else:
                                continue
                        else: # Case it has no mask input
                            if n.name() not in snin: # and node about to be connected not connected already
                                if snci < snmx: # and is within the available inputs
                                    sn.setInput(snci, n)
                                else: # reconnect the last input
                                    sn.setInput(snmx-1, n)
                            else:
                                continue
                                
                    else: # Deal with the exceptions classes
                        
                        # Exception 1
                        if sn.Class() in excp1 and n.Class() in excp1:
                            n.setInput(0, sn)
                        elif sn.Class() in excp1 and n.Class() not in excp1: 
                            sn.setInput(0, n)
                            
                        # Exception 2
                        if sn.Class() in excp2:
                            if n.name() not in snin:
                                if snci == 0:
                                    sn.setInput(0, n)
                                else:
                                    sn.setInput(1, n)