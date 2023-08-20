from __future__ import with_statement

import nuke
import os
import glob
import re

import scl.pipeline.scanPath as scanPath
import scl.nuke.getSequence as getSequence
import scl.nuke.getCamera as getCamera

## define constants
NODE_PATH_EMPTY=1
NODE_PATH_FILLED=2
NODE_PATH_ENABLED=4
NODE_PATH_DISABLED=8


def makeBackdrop(nodes):
    
    import nuke
    
    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in nodes])
    bdY = min([node.ypos() for node in nodes])
    bdW = max([node.xpos() + node.screenWidth() for node in nodes]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in nodes]) - bdY
    
    # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
    left, top, right, bottom = (-10, -80, 10, 100)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)
        
    n = nuke.nodes.BackdropNode(xpos = bdX,
                              bdwidth = bdW,
                              ypos = bdY,
                              bdheight = bdH,
                              note_font_size=42,
                              label="mattes - %s -%s"%(scanPath.getResourceName(nodes[0]['file'].value()), scanPath.getVersionName(nodes[0]['file'].value())))
 
    return n

def createRead_button(path):
    
    first = nuke.thisNode()['first'].value()
    last = nuke.thisNode()['last'].value()
    with nuke.root():
        r = nuke.createNode("Read", inpanel=False)
        r['file'].setValue(path)
        r['first'].setValue(first)
        r['last'].setValue(last)

def loadCamera_button():
    
    node = nuke.thisNode()
    beautyNode = nuke.toNode(nuke.tcl("topnode %s"%node.name()))
    with nuke.root():
        getCamera.getCameraFromNode(beautyNode)        

def loadMattes_button():
    
    node = nuke.thisNode()
    first = nuke.thisNode()['first'].value()
    last = nuke.thisNode()['last'].value()
    beautyNode = nuke.toNode(nuke.tcl("topnode %s"%node.name()))
    versionPath = scanPath.getVersionPath(beautyNode['file'].value())
    mattes = glob.glob(versionPath + "/*matte*")
    reads = []
    for m in sorted(mattes):
        seqPath = scanPath.getSeqPathFromPassPath(m)
        with nuke.root():
            r = nuke.createNode("Read", inpanel=False)
            r['file'].setValue(seqPath)
            r['first'].setValue(first)
            r['last'].setValue(last)
            reads.append(r)
    
    #make a grid of matte nodes
    ydx = 0
    xdx = 0
    idx = 0
    xpos = node['xpos'].value() + 150
    ypos = node['ypos'].value()
    for r in reads:
        print "idx:", xpos + 150*(xdx%3), ypos + 150*ydx
        r.setXYpos(xpos + 150*(xdx%3), ypos + 150*ydx)
        if xdx%3 == 2:
            ydx += 1    
        
        xdx += 1
        idx += 1
    
    with nuke.root():
        makeBackdrop(reads)
    

def loadPasses_button():

    thisNode = nuke.thisNode()    
    updatePasses(thisNode, useBeautyInput=True, verbose=True)
    

def getPathFrames(curPath):

    '''
    if "JPG_" in curPath:
        ext = ".jpg"
    else:
        ext = ".exr"
    
    fileList = os.listdir(curPath)
    exrList  = []
    for basename in fileList:
        if os.path.splitext(basename)[-1] == ext:
            if not '.fctmp.' in basename:
                exrList.append(basename)
    exrList    = sorted(exrList)
    firstFrame = exrList[0].split('.')[-2]
    lastFrame  = exrList[-1].split('.')[-2]
    padding    = len(firstFrame)
    baseFile   = '.'.join(exrList[0].split('.')[:-2])
    pathFrames = curPath + baseFile + '.%0' + str(padding) + 'd%s '%ext + str(firstFrame) + '-' + str(lastFrame)
    '''

    curPath = curPath.rstrip("/")

    #"path first-last"
    seqDicts = getSequence.getDicts(curPath)
    if not seqDicts:
        return ''

    if not "%" in seqDicts[0]['path']:
        return ''
        
    pathFrames = "%s %s-%s"%(seqDicts[0]['path'], seqDicts[0]['first'], seqDicts[0]['last'])
    
    return pathFrames

def determineEnabled(node):
    '''
    Using bitwise math to determine status of paths.
    i.e. the combination of filled/empty and enabled/disabled.
    @node: nukeNode
    @return: status dictionary
    '''

    statusDict = {}
    if node.Class() == 'Group':
        node.begin()
        
    for passNode in nuke.allNodes("Read"):
        currentBitFlags = 0
        
        ## set bit flag for filepath empty or filled
        passName = passNode.name()
        if not passNode['file'].value():
            currentBitFlags |= NODE_PATH_EMPTY
        else:
            currentBitFlags |= NODE_PATH_FILLED
        
        ## set bit flag for enabled/disabled
        enablePassKnobName = "enable_%s" % (passNode.name().lower())
        if node.knob(enablePassKnobName):
            if node.knob(enablePassKnobName).value():
                currentBitFlags |= NODE_PATH_ENABLED
            else:
                currentBitFlags |= NODE_PATH_DISABLED
                
        statusDict[passName] = currentBitFlags

    if node.Class() == 'Group':
        node.end()
        
    return statusDict


def updatePasses(node, useBeautyInput=False, verbose=False):
    '''
    useBeautyInput=True means the passes are being updated in a RenderPass_LOAD_v# node
    useBeautyInput=False means the passes are being updated in a RenderPasses_v# node
    '''

    statusDict = {}
    if useBeautyInput:
        statusDict = determineEnabled(node)

    print node
    if node.Class() == 'Group':
        node.begin()

    if useBeautyInput:
        ## find new path based on incoming connection.  Passes will be loaded based on this.

        beautyNode = nuke.toNode(nuke.tcl("topnode %s"%node.name()))
        
        if (not beautyNode) or (not beautyNode.Class() in ['Read', "ReadBot"]):
            nuke.message("Please connect a 'beauty pass' Read Node to the input of '%s'"%node.fullName())
            return
            
        beautyFilePath = beautyNode['file'].value().replace("\\", "/")
        versionPath = os.path.dirname(os.path.dirname(beautyFilePath)).replace("\\", "/")
        
    else:
        pathPrompt = 'Please enter the base path of the latest renders:\nformat: .../scenes/(shot_name)/images/(folder)/(asset_name_version)/'
        p = nuke.Panel('Update Render Passes')

        try :
            prevVersionPath = '/'.join(nuke.toNode('beauty')['file'].value().split('/')[:-2])
        except :
            prevVersionPath = ''
            
        p.addFilenameSearch(pathPrompt, prevVersionPath)
        p.setWidth(1200)

        success = p.show()
        if not success :
            return

        versionPath = p.value(pathPrompt).strip()

    versionPath = versionPath.replace("\\", "/")
    versionPath.rstrip("/")
    versionPath += '/'

    first = 0
    last = 0

    if nuke.toNode(nuke.tcl("topnode %s"%node.name())) and nuke.toNode(nuke.tcl("topnode %s"%node.name())).Class() in ['Read', "ReadBot"]:
        beautyNode = nuke.toNode(nuke.tcl("topnode %s"%node.name()))
        first = beautyNode['first'].value()
        last = beautyNode['last'].value()
        node['first'].setValue(first)
        node['last'].setValue(last)
        
    versionName = versionPath.split("/")[-2]

    #update the label
    updatedLabel = versionName
    if useBeautyInput:
        if node.knob('UNPREMULT_ALL'):
            updatedLabel = "\n" + versionName + "\n"
            updatedLabel += "[if {[value UNPREMULT_ALL]} {return UNPREMULT} else {return _}]"
    node['label'].setValue(updatedLabel)

    resTag = 'hd'
    passNames = os.listdir(versionPath)
    for passName in passNames:
        tags = passName.split('_')
        if tags[0] == 'beauty':
            resTag = "_".join(tags[1:])
            
    ## if we are re-loading passes, take note of newly available ones
    newlyAddedPasses = []
    for passNode in nuke.allNodes("Read"):
        print '-----------'
        passDir = versionPath + passNode.name() + "_" + resTag + "/"
        enablePassKnobName = "enable_%s" % (passNode.name().lower())

        if os.path.exists(passDir):

            #you found a pass! only update if they have this switch off
            #
            if not node['maintain_paths_on_off'].value():

                if enablePassKnobName in node.knobs():
                    node.knob(enablePassKnobName).setValue(False)
                    newlyAddedPasses.append(passNode.name())
                            
                else:
                    passNode['disable'].setValue(True)
                    
        else:
            #you COULDNT FIND THAT SHJIT
            #
            print 'Could not find: ' + passDir
            #
            if node.knob(enablePassKnobName):
                #disable that sjit via expression!
                #
                node.knob(enablePassKnobName).setValue(False)
            else:
                #disable thats jit directly!
                #
                passNode['disable'].setValue(True)

            #erase the evidence
            #
            passNode['file'].setValue('')
            passNode['proxy'].setValue('')
            
            #change node label in same way Local Proxy Unlink works
            #
            curLabel = passNode.knob('label').value()
            passNode.knob('label').setValue(curLabel.replace('\nPROXY',''))
            
            print 'Just disabled Read: ' + passNode.name()
            continue


        shotName = versionPath.replace("\\", "/").rstrip("/").split("/")[-5]
        resourceName = versionPath.replace("\\", "/").rstrip("/").split("/")[-2]
        version = versionPath.replace("\\", "/").rstrip("/").split("/")[-1].split("_")[0]
        passName = passNode.name()
        baseName = "_".join([shotName, resourceName, passName, version + ".%04d.exr"])
        seqPath = "%s/%s/%s"%(versionPath.rstrip("/"), passNode.name() + "_" + resTag, baseName)

        #set the path you just found
        #
        passNode['file'].setValue(seqPath)

        #set the frame range if its the deprecated node
        #
        if not 'first' in node.knobs():
            pathFrames = getPathFrames(passDir)
            seqPath = pathFrames.split(' ')[0]
            firstFrame = int(pathFrames.split(' ')[1].split("-")[0])
            lastFrame = int(pathFrames.split(' ')[1].split("-")[1])
            passNode['first'].setValue(firstFrame)
            passNode['last'].setValue(lastFrame)
        
        #erase the proxy evdience
        #
        passNode['proxy'].setValue('')
        passNode.knob('label').setValue(passNode.knob('label').value().replace('\nPROXY',''))
        

    if node.Class() == 'Group':
        node.end()
        
    if verbose:
        if newlyAddedPasses:
            ## let user know if new passes (that are currently OFF) have been added since last Load.
            ## NOTE: this message does not show when Load Passes is clicked for the first time on a Fresh node.
            newlyAddedMsg = "New Passes (that currently are OFF)\n\n%s\n\n" % versionName
            newlyAddedMsg += ", ".join(newlyAddedPasses)
            if nuke.env['gui']:
                nuke.message(newlyAddedMsg)
            print newlyAddedMsg

    return
    
