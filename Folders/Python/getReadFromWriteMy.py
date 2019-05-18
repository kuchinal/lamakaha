def getReadFromWriteMy():
    import nuke
    import nukescripts
    from os import listdir
    WriteNodes = [node for node in nuke.selectedNodes() if node.Class()=='Write']
    for node in nuke.selectedNodes():
        fullPath = node['file'].getValue()
        folder = fullPath.rpartition("/")[0]        
        allFiles =  listdir(folder)
        all = []
        for file in allFiles:
            file = file.rpartition(".")[0]
            file = file.rpartition(".")[2]
            file = int(file)
            all.append(file)
        all.sort()
        minimum = all[0]
        maximum = all[-1]
        print minimum, maximum

        readNode = nuke.createNode('Read')
        readNode['file'].setValue(fullPath)
        readNode['xpos'].setValue(node['xpos'].getValue())
        readNode['ypos'].setValue(node['ypos'].getValue()+100)

        readNode['first'].setValue(minimum)
        readNode['last'].setValue(maximum)
        readNode['origfirst'].setValue(minimum)
        readNode['origlast'].setValue(maximum)
