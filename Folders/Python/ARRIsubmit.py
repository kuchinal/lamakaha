import nuke
import arrinuke
import rushnuke

def ARRIsubmit():
    try :
        g = nuke.selectedNode()
        f = nuke.allNodes("Write")
        f = nuke.allNodes("MainFileOut")+f
        f = nuke.allNodes("QTSeqOut")+f
        for a in f:
            sel = a['selected'].value()
            if sel == 1:
                a['disable'].setValue(0)
            else:
                a['disable'].setValue(1)
        arrinuke.autoSaveScript()
        print "selected"
        rushnuke.submitRushJob("nnorm")
    except:
        arrinuke.autoSaveScript()
        rushnuke.submitRushJob("nnorm")
        print "all"