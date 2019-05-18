import nuke
def print_keys():
    n = nuke.thisNode()
    k = nuke.thisKnob()
    name =  k.label()
    #print knob
    try:
        array_size = len(n[knob].value())
    except:
        array_size = 1
    print array_size
    if array_size ==4:
        animCurveX = k.animation( 0 ) #ANIMATION IN THE FIRST FIELD (X VALUE)
        animCurveY = k.animation( 1 ) #ANIMATION IN THE SECOND FIELD (Y VALUE)
        animCurveZ = k.animation( 2 ) #ANIMATION IN THE SECOND FIELD (Z VALUE)
        animCurveW = k.animation( 3 ) #ANIMATION IN THE SECOND FIELD (W VALUE)
        for key in animCurveX.keys():
            xValueX = key.x
            yValueX = key.y
            print '%s X at %s has value %s' % ( name, xValueX, yValueX )
        print "-------------------------"
        for key in animCurveY.keys():
            xValueY = key.x
            yValueY = key.y
            print '%s Y at %s has value %s' % ( name, xValueY, yValueY )
        print "-------------------------"
        for key in animCurveZ.keys():
            xValueZ = key.x
            yValueZ = key.y
            print '%s Z at %s has value %s' % ( name, xValueZ, yValueZ )
        print "-------------------------"
        for key in animCurveW.keys():
            xValueW = key.x
            yValueW = key.y
            print '%s Z at %s has value %s' % ( name, xValueW, yValueW )
        print "-------------------------"

    if array_size ==3:
        animCurveX = k.animation( 0 ) #ANIMATION IN THE FIRST FIELD (X VALUE)
        animCurveY = k.animation( 1 ) #ANIMATION IN THE SECOND FIELD (Y VALUE)
        animCurveZ = k.animation( 2 ) #ANIMATION IN THE SECOND FIELD (Z VALUE)
        for key in animCurveX.keys():
            xValueX = key.x
            yValueX = key.y
            print '%s X at %s has value %s' % ( name, xValueX, yValueX )
        print "-------------------------"
        for key in animCurveY.keys():
            xValueY = key.x
            yValueY = key.y
            print '%s Y at %s has value %s' % ( name, xValueY, yValueY )
        print "-------------------------"
        for key in animCurveZ.keys():
            xValueZ = key.x
            yValueZ = key.y
            print '%s Z at %s has value %s' % ( name, xValueZ, yValueZ )
        print "-------------------------"

    if array_size ==2:
        animCurveX = k.animation( 0 ) #ANIMATION IN THE FIRST FIELD (X VALUE)
        animCurveY = k.animation( 1 ) #ANIMATION IN THE SECOND FIELD (Y VALUE)
        for key in animCurveX.keys():
            xValueX = key.x
            yValueX = key.y
            print '%s X at %s has value %s' % ( name, xValueX, yValueX )
        print "-------------------------"
        for key in animCurveY.keys():
            xValueY = key.x
            yValueY = key.y
            print '%s Y at %s has value %s' % ( name, xValueY, yValueY )
        print "-------------------------"

    if array_size ==1:
        animCurveX = k.animation( 0 ) #ANIMATION IN THE FIRST FIELD (X VALUE)
        l = []
        for key in animCurveX.keys():
            xValueX = key.x
            yValueX = key.y
            x = '%s X at %s has value %s' % ( name, xValueX, yValueX )
            l.append(x)
        o = ""
        for one in l:
            o =  o + one + "\n"

        nuke.message(o)




