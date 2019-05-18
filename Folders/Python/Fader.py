
import nuke
import nukescripts
def Fader():
    curFrameA = nuke.frame()
    inFrame = nuke.frame()-1
    outFrame = nuke.frame()+1
    n = nuke.thisNode()
    k = nuke.thisKnob()
    curValue = k.getValue()
    k.setAnimated()


    class ShapePanel(nukescripts.PythonPanel):
        def __init__(self):
            nukescripts.PythonPanel.__init__(self, 'Fader menu')

            self.Value = nuke.Array_Knob("value",'value',4)
            self.Value.setValue(0,0)
            self.Value.setValue(curValue,1)
            self.Value.setValue(curValue,2)
            self.Value.setValue(0,3)

            self.Frame = nuke.Array_Knob("frame",'frame',4)
            self.Frame.setValue(inFrame,0)
            self.Frame.setValue(curFrameA,1)
            self.Frame.setValue(curFrameA,2)
            self.Frame.setValue(outFrame,3)

            self.Check = nuke.Boolean_Knob('Delete Current Animation')
            self.addKnob(self.Check)

            for k in (self.Frame,self.Value):
                self.addKnob(k)

    ### displays panel
    p = ShapePanel()
    p.showModalDialog()


    ### checks the checkerboard and deletes the animation if selected
    getCheck = p.Check.value()

    if getCheck == True:
        for curve in k.animations():
            curve.clear()



    ### creates the animation
    inV = p.Value.value(0)
    inF = p.Frame.value(0)
    k.setValueAt(inV,inF)

    curV = p.Value.value(1)
    curF = p.Frame.value(1)
    k.setValueAt(curV,curF)

    curVopt = p.Value.value(2)
    curFopt = p.Frame.value(2)
    k.setValueAt(curVopt,curFopt)

    outV = p.Value.value(3)
    outF = p.Frame.value(3)
    k.setValueAt(outV,outF)
 