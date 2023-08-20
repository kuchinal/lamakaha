import nuke




def Label():
    panel = nuke.Panel("Label me!!!")
    panel.addSingleLineInput("Label:","")
    if panel.show():
        i = panel.value("Label:")
        n = nuke.selectedNodes()
        for n in n:

            n['label'].setValue(i)

            n['note_font_size'].setValue(14)
            x = n.xpos()
            y = n.ypos()
            n.setXYpos(x,y-15)
            if n.Class() == "BackdropNode":
                n['note_font_size'].setValue(70)
            if n.Class()== "Dot":
                n['note_font_size'].setValue(30)
                posx = int(n['xpos'].value())
                posy = int(n['ypos'].value())
                n.setXYpos(posx,posy+15)
                n['label'].setValue(i)
            
            
            
def Label_v01():
    panel = nuke.Panel("Bold")
    panel.addSingleLineInput("Name:","")
    if panel.show():
        i = panel.value("Name:")
        n = nuke.selectedNodes()
        for n in n:
            label = n["label"].value()
            if label == "":
                n['label'].setValue(i)
            else:
                n['label'].setValue(i + " \n" +label)
            n['note_font_size'].setValue(14)
            x = n.xpos()
            y = n.ypos()
            n.setXYpos(x,y-15)
            if n.Class() == "BackdropNode":
                n['note_font_size'].setValue(70)
            if n.Class()== "Dot":
                n['note_font_size'].setValue(30)
                posx = int(n['xpos'].value())
                posy = int(n['ypos'].value())
                n.setXYpos(posx,posy+15)
                n['label'].setValue(i)
