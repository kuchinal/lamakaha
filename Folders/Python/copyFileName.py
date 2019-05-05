
import nuke
try:
    from PySide import QtCore, QtGui
except:
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
    qclip = QtGui.QApplication.clipboard() 
    qclip.clear() 
    qclip.setText(l)