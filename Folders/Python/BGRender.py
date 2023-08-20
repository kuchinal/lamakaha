import nuke
import nukescripts
def BGRender():
    write = nuke.selectedNode()
    Name  = write['name'].value()
    first  = nuke.toNode("root")['first_frame'].value()
    first = int(first)
    first = str(first)
    last  = nuke.toNode("root")['last_frame'].value()
    last = int(last)
    last = str(last)
    G = path = nuke.env['ExecutablePath']    # nuke location
    Y = nuke.Root().knob('name').getValue()       # project name
    panel = nuke.Panel("BG Render")
    panel.addSingleLineInput("Run Me:",u"\u0022" +  G + u"\u0022" +  " -X "+ " " + Name+" " + Y + " "  +  first + ","+ last )
    panel.setWidth(700)
    panel.show()
    nuke.scriptSave()
    nukescripts.start("C:\WINDOWS\system32\cmd.exe")
