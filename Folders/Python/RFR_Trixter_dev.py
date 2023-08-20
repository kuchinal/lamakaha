import nuke
import nukescripts
from os import listdir

def settingCheck():
    rootNode = nuke.toNode("root")
    try:
        pan=rootNode['r_viewer'].value()
    except:
        rootNode.addKnob(nuke.Enumeration_Knob("r_viewer","reference viewer",["1","2","3","4","5","6","7","8","9","0","ignore"]))

        panel = nuke.Panel("set default reference input")
        panel.addEnumerationPulldown("Please select which viewer input you would like to use as a default for your reference render\nThis message will appear only once and result will be saved for the followed sessions\nIf you do not want to have default reference input please select 'ignore'\n you will be able to change this behaviour later in project settings", "1 2 3 4 5 6 7 8 9 0 ignore")
        r = panel.show()
        if r == 1:
            pan = panel.value("Please select which viewer input you would like to use as a default for your reference render\nThis message will appear only once and result will be saved for the followed sessions\nIf you do not want to have default reference input please select 'ignore'\n you will be able to change this behaviour later in project settings")
            if "ignore" not in pan:
                refShortcutKnob=rootNode['r_viewer'].setValue(pan)
    return pan



#reload all read nodes in the script
def reloadReads():
    r = nuke.allNodes()
    for a in r:
        if "Read" in a.Class():
            a['reload'].execute()
#create read from write
def RFRTrixter(n,nukeV):

    noDirect = 2
    WriteNodes = [node for node in nuke.selectedNodes() if'Write' in node.Class()]
    for node in nuke.selectedNodes():
        if 'Write' in node.Class() or node.Class() == "Group":
            try:
                f = int(node['first'].value())
                l = int(node['last'].value())
                u = node['use_limit'].value()
            except:
                pass
            fullPath = node['file'].getValue()
            folder = fullPath.rpartition("/")[0] 
            try:
                allFiles =  listdir(folder)
                all = []
                for file in allFiles:
                    if ".tmp" not in file:
                        all.append(int(file.rpartition(".")[0].rpartition(".")[2]))
                all.sort()
                minimum = int(all[0])
                maximum = int(all[-1])
                
            except:
                minimum = int(nuke.root()['first_frame'].getValue())
                maximum = int(nuke.root()['last_frame'].getValue())
                nuke.message("Cant find directory")
                noDirect = 1
            try:
                vers=node['rendered_version'].value()
            except:
                vers = ""
            if "Deep" in node.Class():
                readNode = nuke.createNode('DeepRead')
            else:
                readNode = nuke.createNode('Read')
            readNode['file'].setValue(fullPath)
            readNode['xpos'].setValue(int(node['xpos'].getValue()))
            readNode['ypos'].setValue(int(node['ypos'].getValue()+85))
            readNode['first'].setValue(minimum)
            readNode['last'].setValue(maximum)
            readNode['origfirst'].setValue(minimum)
            readNode['origlast'].setValue(maximum)
            readNode['label'].setValue(vers)
            break
    return (noDirect,readNode,f,l,u)
#file out section in the nuke start template
def fileOutRFW(noDirectory):
    defViewerConnect = settingCheck()
    print defViewerConnect
    n =  nuke.selectedNode()
    xo = int(n['xpos'].value())
    yo = int(n['ypos'].value())

    index = n['file'].value().find('_v')
    version =  n['file'].value()[index+1:index+6]
    n['label'].setValue(version)
    n.setSelected(True)
    n.setXYpos(xo,yo+85)
    ### moving old results down
    a = nuke.allNodes("Read")
    a.remove(n)
    for node in a:
        y = int(node['ypos'].value())
        x = int(node['xpos'].value())
        if x> xo-40 and x< xo+40 and y> yo:
            node.setXYpos(x,y+60)
            node.setSelected(False)
    if "ignore" not in defViewerConnect:
        nukescripts.connect_selected_to_viewer(int(defViewerConnect)-1)
    n.setSelected(True)
    nuke.activeViewer().node().setSelected(False)
#precomp section 
def precompRFW(myBD,writeNode,x,y,xb,yb,bdW,bdH,noDirectory,nukeV,readNode,f,l,u):
    ba = myBD
    print xb," / ",yb," / ",bdW," / ",bdH

    ba['tile_color'].setValue(2466250752L)

    x = int(readNode['xpos'].value())
    y = int(readNode['ypos'].value())

    new =  readNode['name'].value()
    b = nuke.allNodes("Read")+nuke.allNodes("DeepRead")

    for a in b:
        xa = a['xpos'].value()
        ya = a['ypos'].value()
        
        if  xa>x-50 and xa<x+50  and ya>y-50 and ya<y+50 :
            print "read ", xa," / ",ya
            g = a['name'].value()
            if new in g:
                fresh = readNode
                fresh.setXYpos(x,y-22)
                if u == 1:
                    fresh['first'].setValue(f)
                    fresh['last'].setValue(l)
            else:
                d = a['name'].value()
                nuke.delete(a)
            break

    d = nuke.allNodes("Dot")
    for dot in d:
        xa = dot['xpos'].value()
        ya = dot['ypos'].value()
        dotLabel = dot['label'].value()
        
        if  xa>xb and xa<bdW  and ya>yb and ya<bdH :
            if "OUT" in dotLabel:
                print "dot", xa,"/",ya
                dot.setInput(0,fresh)
                break
    if noDirectory == 0:
        panel = nuke.Panel("localise? it is important!")
        panel.addBooleanCheckBox('localise', False)
        panel.show()
        i = panel.value("localise")
        if i == 1:
            if nukeV < 10:
                doLocalise(0)
            else:
                readNode['localizationPolicy'].setValue("on")
            reloadReads()
        else:
            if nukeV < 10:
                pass
            else:
                readNode['localizationPolicy'].setValue("off")
            reloadReads()
#localise activation
def localiseNode(n,nukeV):
    panel = nuke.Panel("localise? it is important!")
    panel.addBooleanCheckBox('localise', False)
    panel.show()
    i = panel.value("localise")
    if i == 1:
        if nukeV < 10:
            doLocalise(0)
        else:
            n['localizationPolicy'].setValue("on")
        reloadReads()
    else:
        if nukeV < 10:
            pass
        else:
            n['localizationPolicy'].setValue("off")
        reloadReads()
#main function
def RFRmain():
    foundBackDrop = 0
    n =  nuke.selectedNodes()
    b=n
    b.reverse()
    cl = b[0].Class()
    # write node selected
    if len(n) == 1 and "Write" in n[0].Class():
        x = int(n[0]['xpos'].value())
        y = int(n[0]['ypos'].value())
        b = nuke.allNodes("BackdropNode")
        #looking for a relevant backdrop
        for ba in b:
            xb = int(ba['xpos'].value())
            yb = int(ba['ypos'].value())
            bdW = xb+ba['bdwidth'].value()
            bdH = yb+ba['bdheight'].value()
            #find backdrop
            if x>xb and x< bdW and y>yb and y<bdH:
                myBD = ba
                foundBackDrop = 1
                xb = int(ba['xpos'].value())
                yb = int(ba['ypos'].value())
                bdW = xb+ba['bdwidth'].value()
                bdH = yb+ba['bdheight'].value()
                break
        writeNode = n[0]

        nukeV = nuke.NUKE_VERSION_MAJOR
        if nukeV > 9:
            nuke.localization.resumeLocalization()
        #looking for special cases when write node is inside of the backdrop
        if foundBackDrop == 1:
            # file out case
            if myBD['label'].value()== "File Out":
                noDirectory, readNode,f,l,u= RFRTrixter(writeNode,nukeV)
                fileOutRFW(noDirectory)
            # precomp case
            elif "Precomp" in myBD['label'].value():
                noDirectory, readNode,f,l,u= RFRTrixter(writeNode,nukeV)
                precompRFW(myBD,writeNode,x,y,xb,yb,bdW,bdH,noDirectory,nukeV,readNode,f,l,u)
        # no special case, simple read from write
        else:
            noDirectory, readNode,f,l,u= RFRTrixter(writeNode,nukeV)
        # if newly created read node has directory - ask for the localization
        if noDirectory == 2:
            localiseNode(nuke.selectedNode(),nukeV)
    #if backdrop is selected

    elif "Backdrop" in cl:
        for node in nuke.selectedNodes():
            label = node['label'].value()
            if label == "IN":
                IN = node
            elif label =="OUT":
                OUT = node
            elif "Precomp" in label:
                PREC = node
        OUT.setInput(0,IN)
        PREC['tile_color'].setValue(4294967295)


# reload(RFR_Trixter_dev)
# RFR_Trixter_dev.RFRmain()