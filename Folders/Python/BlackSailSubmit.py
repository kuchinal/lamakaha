
import nuke
import rrSubmit_Nuke_5
def BlackSailSubmit():
    try :
        g = nuke.selectedNode()
        f = nuke.allNodes("Write")
        f= nuke.allNodes("AutoWrite")+f
        for a in f:
            sel = a['selected'].value()
            if sel == 1:
                a['disable'].setValue(0)
            else:
                a['disable'].setValue(1)
        print "selected"
        rrSubmit_Nuke_5.rrSubmit_Nuke_5()
    except:
        rrSubmit_Nuke_5.rrSubmit_Nuke_5()
        print "all"