import nuke
def copyFileName():
    try:
        from PySide import QtCore, QtGui, QtGui as QtWidgets 
    except:
        from PySide2 import QtWidgets, QtCore, QtGui 

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

    qclip = QtWidgets.QApplication.clipboard() 
    qclip.clear() 
    qclip.setText(l)