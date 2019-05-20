import nuke
def cameras():
    n = nuke.selectedNodes()
    x=0
    for i in n:
        if x == 2:
            i['label'].setValue("Left Cam")
        if x == 1:
            i['label'].setValue("Middle Cam")
        if x == 0:
            i['label'].setValue("Right Cam")
        x=x+1