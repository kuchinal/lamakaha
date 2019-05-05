
'''
Created on 19-jan-2013
Updated on 2 april 2016
@author: satheesh-R
mail - satheesrev@gmail.com
modified by Alexey Kuchinski
'''
try:
    from PySide import QtCore, QtGui
except:
    from PySide2 import QtCore, QtGui

import nuke, nukescripts 
import getpass

def saveImage ():
    user = getpass.getuser()
    defaultPath = "/mnt/user/share/"+user+"/"
    ### Getting Lut list from root
    LutList = [n.split(" ")[0] for n in nuke.root()['luts'].toScript().split("\n")]
    Luts = '\n'.join(LutList)

    ### creating panel and assign buttons
    ef = nuke.Panel("saveImage As......  by satheesh-r", 420)
    ef.addSingleLineInput("Name:","")
    ef.addFilenameSearch("Save Image As:", defaultPath)
    ef.addButton("cancel")
    ef.addEnumerationPulldown('channels', "rgb rgba all")
    ef.addEnumerationPulldown('Color Space', "sRGB "+Luts)
    ef.addEnumerationPulldown('Exr data type', "16bit-half 32bit-float")
    ef.addButton("ok")
    window=ef.show()

    ### getting values from panel
    exrtype = ef.value('Exr data type')
    channel = ef.value('channels')
    path = ef.value("Save Image As:")+ef.value("Name:")
    colorSpace = ef.value('Color Space')
    if colorSpace=="sRGB":
        path=path+".jpg"
    fileType = path.split('.')[-1]

    ### User cancel the oparation
    if window == 0 :
        return

    ### if file format not found
    fileFormat = path.split('/')[-1]
    findDot = ('.')
    for dot in findDot:
        if dot in fileFormat:
            if dot == '.':
            
                ### getting path from user input
                if path == "":
                    nuke.message('no file path selected ')
                if path == "":
                    return
            
                ### getting active node
                curViewer = nuke.activeViewer()
                curNode = curViewer.node()
                acticeVinput = curViewer.activeInput()
                curN = curNode.input(acticeVinput)

                ### setting current frame for render
                curFrame = nuke.frame()
                if curFrame =="":
                  curFrame = curFrame 
          
                ### creating temp write
                w = nuke.createNode("Write")
                w.setName("tempWrite")
                w.setInput(0, curN)
                path = path.replace(".",str(curFrame)+".")
                w['file'].setValue(path)
                w['colorspace'].setValue(colorSpace)
                w['channels'].setValue(channel)
            
                ### if file type is jpg
                if fileType == 'jpg' :
                    w['_jpeg_sub_sampling'].setValue(2)
                    w['_jpeg_quality'].setValue(1)
                    w['raw'].setValue(0)
                    w['colorspace'].setValue("sRGB")
            
                ### if file type is exr
                if fileType == 'exr' :
                    w['datatype'].setValue(exrtype)
                    w['compression'].setValue(2)
                    w['metadata'].setValue(0)
            

                ### creating the text node for the frame number
                
                ### execute write node
                nuke.execute(nuke.selectedNode(), (int(curFrame)), curFrame)
                name = w.knob('file').value()
                nukescripts.node_delete(popupOnError=True)
            
                ### create Read node
                r = nuke.createNode("Read")
                r['file'].setValue(name)
                curFrame = nuke.frame()
                r['first'].setValue(int(curFrame))
                r['last'].setValue(int(curFrame))
                r["reload"].execute()
                r['raw'].setValue(0)
                r['colorspace'].setValue("sRGB")
        else:
            nuke.message('forget to choose file format')
            return
    s_text = name 
    qclip = QtGui.QApplication.clipboard() 
    qclip.clear() 
    qclip.setText(s_text) 

#saveImage ()
