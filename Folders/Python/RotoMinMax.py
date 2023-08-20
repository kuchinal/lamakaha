import nuke
def RotoMinMax():
    try:
        n = nuke.selectedNode()
        if n.Class()== "RotoPaint":
            print "rotopaint selected"
            t = n['toolbar_blending_mode'].value()
            if t == "max":
                n['toolbar_blending_mode'].setValue("min")
                n['gl_color'].setValue(1063467008L)
                
            elif t == "min":
                n['toolbar_blending_mode'].setValue("over")  
                n['gl_color'].setValue(4294967295)

            elif t == "over":
                n['toolbar_blending_mode'].setValue("max")  
                n['gl_color'].setValue(2600468735) 
            else:
                n['toolbar_blending_mode'].setValue("over")  
                n['gl_color'].setValue(4294967295)

        elif n.Class()== "Roto":
            auto = n['toolbar_autokey']
            t=auto.value()
            if t == 0:
                auto.setValue(1)
                n['gl_color'].setValue(1063467008L)
                
            elif t == 1:
                auto.setValue(0)  
                n['gl_color'].setValue(1717789695)

    except:
        print "no roto node selected"
        import traceback; traceback.print_exc()
      