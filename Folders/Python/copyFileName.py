
import nuke
try:
    from PySide import QtCore, QtGui
except:
    import PySide2
    from PySide2 import QtCore, QtGui

def copyFileName():
    a= nuke.selectedNodes()
    l=""
    for one in a:
            t=one['file'].value()
            if "first" in one.knobs():
                last = one['last'].value()
                first=one['first'].value()
            if "range_first" in one.knobs():
                last = one['range_last'].value()
                first=one['range_first'].value()
            l=l+t+" "+str(first)+"-"+str(last)+"\n"
            print l
    try:
        qclip = QtGui.QApplication.clipboard()
    except:
        PySide2.QtWidgets.QApplication.clipboard() 
    qclip.clear() 
    qclip.setText(l)




