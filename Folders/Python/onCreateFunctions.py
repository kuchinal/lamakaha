import nuke
def onCreateFunctions():

    def wCard():
        if nuke.NUKE_VERSION_MAJOR < 11:
            import PySide
        else:
            import PySide2
        node = nuke.thisNode()
        from cryptomatte_utilities import CryptomatteInfo
        current_layer = CryptomatteInfo(node).selection
        clipboard = PySide2.QtGui.QGuiApplication.clipboard()
        wildcard = clipboard.text()
        #wildcard = node['WildnessLevel'].value()
        in_list = []
        manifest = json.loads(node.metadata("exr/cryptomatte/{0}/manifest".format(current_layer) ))
        for m in manifest.keys():
            if str(m).find(wildcard.
                rstrip("*")) != -1:
                if str(m) not in in_list:
                    in_list.append(str(m))
        out_list = ", ".join(in_list)
        node.knob("matteList").setValue(out_list)
        print "script by Marco Meyer"
    def WildCardButton():
        w = nuke.Text_Knob("W","")
        m = nuke.PyScript_Knob("wildCard","Wild card","wCard()")
        #t = nuke.String_Knob("WildnessLevel","Wildness Level")
        h = nuke.Text_Knob("help","Wild help","\n\n\n1 pick one of objects you want to get with Picker\n2 Manually copy the string from 'Matte List' up to area you do not want to have\n3 press 'Wild Card' button!\n----------------------------\n\n\n Example:\nroot/human/arm/wrist/fingers/fingerA\n If you want to get all the fingers copy:\nroot/human/arm/wrist/fingers/")
        n=nuke.thisNode()
        try:
            n['W']
            pass
        except Exception:
            n.addKnob(w)
            n.addKnob(m)
            #n.addKnob(t)
            n.addKnob(h)
    nuke.addOnCreate(lambda: WildCardButton() , nodeClass="Cryptomatte")

    def csMy():
            try:
                n = nuke.thisNode()
                n['User'].setFlag(0)
            except:
                pass
    nuke.addOnCreate(lambda: csMy(), nodeClass="ContactSheet")

    def cubeFun():  
        a = nuke.PyScript_Knob("floor Pivot","floor Pivot","n=nuke.thisNode()\nn['translate'].setValue([0,0.5,0])\nn['pivot'].setValue([0,-0.5,0])")
        nuke.thisNode().addKnob(a) 
        c = nuke.PyScript_Knob("corner Pivot","corner Pivot","n=nuke.thisNode()\nn['translate'].setValue([-.5,.5,-.5])\nn['pivot'].setValue([.5,-.5,.5])")
        nuke.thisNode().addKnob(c)   
        b = nuke.PyScript_Knob("freeze corners","freeze corners","n=nuke.thisNode()\nn['cube'].setExpression('-0.5',0)\nn['cube'].setExpression('-0.5',1)\nn['cube'].setExpression('-0.5',2)\nn['cube'].setExpression('0.5',3)\nn['cube'].setExpression('0.5',4)\nn['cube'].setExpression('0.5',5)")
        nuke.thisNode().addKnob(b)   
        d = nuke.PyScript_Knob("snapToSelected","snapToSelected","b=nuke.selectedNode()['translate'].value()\nn=nuke.thisNode()\nn['translate'].setValue(b)")
        nuke.thisNode().addKnob(d) 
    nuke.addOnCreate(lambda: cubeFun(), nodeClass="Cube")

    def cylinderFun():  
        a = nuke.PyScript_Knob("floor Pivot","floor Pivot","n=nuke.thisNode()\nn['translate'].setValue([0,1,0])\nn['pivot'].setValue([0,-1,0])")
        nuke.thisNode().addKnob(a)  
        d = nuke.PyScript_Knob("snapToSelected","snapToSelected","b=nuke.selectedNode()['translate'].value()\nn=nuke.thisNode()\nn['translate'].setValue(b)")
        nuke.thisNode().addKnob(d) 
    nuke.addOnCreate(lambda: cylinderFun(), nodeClass="Cylinder")

    def keepLuma():
        n = nuke.thisNode()
        b = n['black'].value()
        w = n['white'].value()
        n['multiply'].setValue(1/((w[0]+w[1]+w[2])/3))
        n['add'].setValue(-(b[0]+b[1]+b[2])/3)
    def keepLumaGrade():  
        a = nuke.PyScript_Knob("keep luma","keep luma","keepLuma()")
        nuke.thisNode().addKnob(a) 
    nuke.addOnCreate(lambda: keepLumaGrade(), nodeClass="Grade")

    def sphereFun():  
        a = nuke.PyScript_Knob("floor Pivot","floor Pivot","n=nuke.thisNode()\nn['translate'].setValue([0,1,0])\nn['pivot'].setValue([0,-1,0])")
        nuke.thisNode().addKnob(a) 
        d = nuke.PyScript_Knob("snapToSelected","snapToSelected","b=nuke.selectedNode()['translate'].value()\nn=nuke.thisNode()\nn['translate'].setValue(b)")
        nuke.thisNode().addKnob(d) 
    nuke.addOnCreate(lambda: sphereFun(), nodeClass="Sphere")

    def cardFun():  
        a = nuke.PyScript_Knob("floor Pivot","floor Pivot","n=nuke.thisNode()\nn['translate'].setValue([0,0.5,0])\nn['pivot'].setValue([0,-0.5,0])")
        nuke.thisNode().addKnob(a) 
        c = nuke.PyScript_Knob("corner Pivot","corner Pivot","n=nuke.thisNode()\nn['translate'].setValue([-.5,.5,0])\nn['pivot'].setValue([.5,-.5,0])")
        nuke.thisNode().addKnob(c)     
        d = nuke.PyScript_Knob("snapToSelected","snapToSelected","b=nuke.selectedNode()['translate'].value()\nn=nuke.thisNode()\nn['translate'].setValue(b)")
        nuke.thisNode().addKnob(d) 
    nuke.addOnCreate(lambda: cardFun(), nodeClass="Card2")
