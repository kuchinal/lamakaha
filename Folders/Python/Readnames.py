def Readnames():
    import nuke
    from PySide import QtCore, QtGui
    n = nuke.selectedNodes()
    a = "Short name:"
    b ='\n'+ '\n'+"Full path:"
    for n in n:
        t= n['file'].value().rpartition("/")[2]
        a = a+"\n"+t
        o = n['file'].value()
        b = b+"\n"+o
    m = str(a+b)
    qclip = QtGui.QApplication.clipboard()
    qclip.clear()
    qclip.setText(m) 
