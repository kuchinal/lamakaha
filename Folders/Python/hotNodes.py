def hotNodes():
    import nuke
    l=nuke.selectedNodes()
    brasil = ["BBM1060","BBM1080","CSG4180","MCR0500","MCR1440","MCR7090 ","MSE1000","MSE1000","MSE1020","MSE1040","MSE1060","MSE1240","MSE1320","MSE1360","MSE1420","MSE1440","MSE1640","MSE1700","MSE1740","MSE1780","MSE1820","MSE1850","MSE1860","MSE2240","MSE2260","MSE2380","MSE2400","MSE2480","MSE2500","MSE2520","MSE2540","MSE2560","MSE2580","MSE2620","MSE2820 ","MSE2840","MSE2860","MSE2880","MSE3200","MSE3220","MSE3300","MSE3320","MSE3340","MSE3360","MSE3420","MSE3440","MSE3460","MSE3480","MSE3500","MSE3580 ","MSE3600","MSE3620","MSE3640","MSE3660","MSE3680","MSE3860","MSE3980","MSE3990","MSE4000","MSE4060","MSE7010"]
    for a in l:
        c = a['name'].value().rpartition("_")[0].partition("_")[2].replace("_","")
        for one in brasil:
            if one in c:
                a.begin()
                try:
                    nuke.toNode("OCIODisplay1").setSelected(True)
                    g = nuke.createNode("Grade")
                    g.setName("red")
                    g['white'].setValue([3,.2,.2,0])
                    a.end()
                except:
                    a.end()



def hotNodesRemove(): 
    import nuke 
    l=nuke.selectedNodes()
    for a in l:

        a.begin()
        try:
            nuke.delete(nuke.toNode("red1"))
            nuke.delete(nuke.toNode("red"))

            a.end()
        except:
            a.end()



def hotNodesNearest(): 
    import nuke 
    l=nuke.selectedNodes()
    for a in l:
        a.begin()
        try:
            nuke.toNode("Read1")['on_error'].setValue("nearest frame")

            a.end()
        except:
            a.end()

hotNodesNearest()