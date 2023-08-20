import nuke
import json

#code for wild card stuff
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