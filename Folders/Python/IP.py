

def Cache():
    import nuke
    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('cached')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0)  
            
def Saturation():
    import nuke

    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('saturation')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0) 
            
def Flip():
    import nuke

    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('flip')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0)  
            
def Flop():
    import nuke

    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('flop')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0)  
            
def Grid():
    import nuke
    new = nuke.toNode("grid")
    nuke.show(new)
    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('grid')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0)

def Lines():
    import nuke
    new = nuke.toNode("Lines")
    nuke.show(new)
    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('Lines')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0)             
            
def InputProcess():
    import nuke

    w = nuke.allNodes("Viewer")
    for one in w:
        one['input_process_node'].setValue('VIEWER_INPUT')
        val = one['input_process'].value()
        if val  == 0 :
            one['input_process'].setValue(1)
        else:
            one['input_process'].setValue(0) 