def ReadnamesSlapcomp():
    import nuke
    from PySide import QtCore, QtGui
    n = nuke.selectedNodes()
    a = "(Slapcomp)"+"\n"+" list of new elements:"
    root = nuke.Root().name().rpartition("/")[2].rpartition("_")[0]
    for n in n:
        t= n['file'].value().rpartition("/")[2]
        a = a+"\n"+t
    m = "\n"+root+"\n"+str(a)
    qclip = QtGui.QApplication.clipboard()
    qclip.clear()
    qclip.setText(m) 