# Original script by Pete O'Connell extended by Alexey Kuchinsky to loop the script over a frame range.
import nuke
def getTheCornerpinAsMatrix():

     projectionMatrixTo = nuke.math.Matrix4()
     projectionMatrixFrom = nuke.math.Matrix4()

     #dir(projectionMatrix)
     theCornerpinNode = nuke.selectedNode()
     theNewCornerpinNode = nuke.createNode("CornerPin2D")
     theNewCornerpinNode['transform_matrix'].setAnimated()

     imageWidth = float(theCornerpinNode.width())
     imageHeight = float(theCornerpinNode.height())

     first = nuke.Root().knob('first_frame').getValue()
     first = int(first)
     last = nuke.Root().knob('last_frame').getValue()
     last = int(last)+1
     frame = first
     while frame<last:
         to1x = theCornerpinNode['to1'].valueAt(frame)[0]
         to1y = theCornerpinNode['to1'].valueAt(frame)[1]
         to2x = theCornerpinNode['to2'].valueAt(frame)[0]
         to2y = theCornerpinNode['to2'].valueAt(frame)[1]
         to3x = theCornerpinNode['to3'].valueAt(frame)[0]
         to3y = theCornerpinNode['to3'].valueAt(frame)[1]
         to4x = theCornerpinNode['to4'].valueAt(frame)[0]
         to4y = theCornerpinNode['to4'].valueAt(frame)[1]
    
         from1x = theCornerpinNode['from1'].valueAt(frame)[0]
         from1y = theCornerpinNode['from1'].valueAt(frame)[1]
         from2x = theCornerpinNode['from2'].valueAt(frame)[0]
         from2y = theCornerpinNode['from2'].valueAt(frame)[1]
         from3x = theCornerpinNode['from3'].valueAt(frame)[0]
         from3y = theCornerpinNode['from3'].valueAt(frame)[1]
         from4x = theCornerpinNode['from4'].valueAt(frame)[0]
         from4y = theCornerpinNode['from4'].valueAt(frame)[1]
    
         projectionMatrixTo.mapUnitSquareToQuad(to1x,to1y,to2x,to2y,to3x,to3y,to4x,to4y)
         projectionMatrixFrom.mapUnitSquareToQuad(from1x,from1y,from2x,from2y,from3x,from3y,from4x,from4y)
         theCornerpinAsMatrix = projectionMatrixTo*projectionMatrixFrom.inverse()
         theCornerpinAsMatrix.transpose()
       
         a0 = theCornerpinAsMatrix[0]
         a1 = theCornerpinAsMatrix[1]
         a2 = theCornerpinAsMatrix[2]
         a3 = theCornerpinAsMatrix[3]    
         a4 = theCornerpinAsMatrix[4]
         a5 = theCornerpinAsMatrix[5]
         a6 = theCornerpinAsMatrix[6]
         a7 = theCornerpinAsMatrix[7]   
         a8 = theCornerpinAsMatrix[8]
         a9 = theCornerpinAsMatrix[9]
         a10 = theCornerpinAsMatrix[10]
         a11 = theCornerpinAsMatrix[11]    
         a12 = theCornerpinAsMatrix[12]
         a13 = theCornerpinAsMatrix[13]
         a14 = theCornerpinAsMatrix[14]
         a15 = theCornerpinAsMatrix[15]
    
         theNewCornerpinNode['transform_matrix'].setValueAt(a0,frame,0)
         theNewCornerpinNode['transform_matrix'].setValueAt(a1,frame,1)
         theNewCornerpinNode['transform_matrix'].setValueAt(a2,frame,2)
         theNewCornerpinNode['transform_matrix'].setValueAt(a3,frame,3)    
         theNewCornerpinNode['transform_matrix'].setValueAt(a4,frame,4)
         theNewCornerpinNode['transform_matrix'].setValueAt(a5,frame,5)
         theNewCornerpinNode['transform_matrix'].setValueAt(a6,frame,6)
         theNewCornerpinNode['transform_matrix'].setValueAt(a7,frame,7)    
         theNewCornerpinNode['transform_matrix'].setValueAt(a8,frame,8)
         theNewCornerpinNode['transform_matrix'].setValueAt(a9,frame,9)
         theNewCornerpinNode['transform_matrix'].setValueAt(a10,frame,10)
         theNewCornerpinNode['transform_matrix'].setValueAt(a11,frame,11)
         theNewCornerpinNode['transform_matrix'].setValueAt(a12,frame,12)
         theNewCornerpinNode['transform_matrix'].setValueAt(a13,frame,13)
         theNewCornerpinNode['transform_matrix'].setValueAt(a14,frame,14)
         theNewCornerpinNode['transform_matrix'].setValueAt(a15,frame,15)
         frame = frame + 1
    
    theNewCornerpinNode.setSelected(True)
    theCornerpinNode.setSelected(False)




