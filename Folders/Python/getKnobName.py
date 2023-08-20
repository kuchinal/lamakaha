import nuke
def getKnobName():
    n = nuke.thisNode()
    k = nuke.thisKnob()
    s_text =  k.name()
    from PySide import QtCore, QtGui
    qclip = QtGui.QApplication.clipboard()
    qclip.clear()
    qclip.setText(s_text)