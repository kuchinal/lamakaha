import nuke
import json
def wildcard():
    node = nuke.selectedNode()
    from cryptomatte_utilities import CryptomatteInfo
    current_layer = CryptomatteInfo(node).selection
    wildcard = nuke.getInput("Please enter wildcard (name of the object,just copy it):", "*")
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


