
import os
import nuke

def  Corner():
 def cop():
    n = nuke.selectedNode()
    a=n['to1'].getValue()
    b=n['to2'].getValue()
    c=n['to3'].getValue()
    d=n['to4'].getValue()
    n['from1'].setValue(a)
    n['from2'].setValue(b)
    n['from3'].setValue(c)
    n['from4'].setValue(d)
   
 o = nuke.createNode("CornerPin2D")
 Button = nuke.PyScript_Knob('Copier')                   #set variation to Button - phython script button
 script = '''nuke.createNode("Blur") '''                                                   # set variation to script - phyton script to exequte
 Button.setValue(script)                                                        # set value into button  - script
 o.addKnob(Button)                                                                # add button to node b
