import nuke
def NameMy():
    panel = nuke.Panel("name me!!!")
    panel.addSingleLineInput("Name:","")
    panel.show()
    name = panel.value("Name:")
    nuke.selectedNode().setName(name)
    nuke.selectedNode()['note_font_size'].setValue(20)
