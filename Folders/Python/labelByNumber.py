import nuke
def labelByNumber():
    panel=nuke.Panel("label me")
    panel.addSingleLineInput("number","")
    panel.addSingleLineInput("separator","_")
    panel.show()
    all = nuke.selectedNodes()
    key = int(panel.value("number"))
    separator = panel.value("separator")
    for n in all:
        name = n["file"].value()
        part = name.split(separator)[key]
        n['label'].setValue(part)
        n['autolabel'].setValue("nuke.thisNode()['label'].value()")
        n['note_font_size'].setValue(20)
