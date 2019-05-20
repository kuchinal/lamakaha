import nuke
def labelByKeyWord():
    panel=nuke.Panel("label me")
    panel.addSingleLineInput("keyWord","")
    panel.show()
    all = nuke.selectedNodes()
    key = panel.value("keyWord")
    for n in all:
        name = n["file"].value()
        #parts = name.split("_")
        list  = name.count("_")
        print list
        x = 0
        while x<list:
            part = name.split("_")[x]
            x = x+1
            print part
            if key in part:
                n['label'].setValue(part)
                n['autolabel'].setValue("nuke.thisNode()['label'].value()")
                n['note_font_size'].setValue(20)