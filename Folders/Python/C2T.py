#C2T new
import thread, threading, time, nuke, math, nukescripts

def execRC(first,last):
    runMe = True
    while runMe == True:
        nuke.execute('r1',first,last)  
        nuke.execute('r2',first,last) 
        nuke.execute('r3',first,last) 
        nuke.execute('r4',first,last) 
        stop_event.set()
        runMe = False
        print 'reconcile done'
        break

def getCamera():
    cameraClasses = ['Camera', 'Camera2']
    redDotColor = 3070231295

    allCamsInScript = []
    for n in nuke.allNodes():
        if n.Class() in cameraClasses:
            allCamsInScript.append(n.name())


    # by selection ...
    for n in nuke.selectedNodes():
        if n.Class() in cameraClasses:
            cam = n
            print 'got camera by selection:', cam.name()
            return cam
            
    # by label ...
    for d in nuke.allNodes(): 
        names = ['MainCam','main_cam','MasterCam','master_cam']
        for one in names:
            if d['label'].value() ==one :
                cam = d
                print 'got camera by label:', cam.name()
                return cam

    # by dropdown ...
    camListPrint = ''
    for c in allCamsInScript:
        camListPrint = camListPrint + c + ' '
    p = nuke.Panel('select camera')
    p.addEnumerationPulldown('camera', camListPrint)
    p.show()
    if p.value('camera'):
        # ok pressed
        cam = nuke.toNode(p.value('camera'))
        print 'got camera by dropdown:', cam.name()
        return cam


def BGdetect():
    for n in nuke.selectedNodes():
        #if 'format' in n.knobs():
        if 'xform_order' not in n.knobs():
            Name = n.name()
            Width = n.width()
            Height = n.height()
            Aspect = n.pixelAspect()
            form = str(Width)+" "+str(Height)+" "+str(Aspect)
            print 'format selected:'+" "+form
            
            bg = nuke.nodes.Constant(postage_stamp = False)
            bg['format'].setValue(nuke.addFormat(form))
            return bg
    #no format found ...
    
    #bg = nuke.createNode('Constant')
    #bg = nuke.nodes.Constant(postage_stamp = False)
    #return bg
        
def C2T(dialog):

    # classes
    cameraClasses = ['Camera', 'Camera2']
    cardClasses = ['Card', 'Card2']

    #card
    card = None
    for n in nuke.selectedNodes():
        if n.Class() in cardClasses:
            card = n
            break
    if card == None:
        nuke.message('no card selected?')
        return


        
        
    # initialize tool values for auto-creation
    label = card['label'].value()
    ref = int(nuke.frame())
    first = int(nuke.Root().knob('first_frame').getValue())
    last = int(nuke.Root().knob('last_frame').getValue())
    bg = BGdetect() 
    cam = getCamera()
    rootAspect = nuke.Root()['format'].value().pixelAspect()
    x = card.xpos() 
    y = card.ypos()
    
    bg.setXYpos(x,y+50)
    
    if dialog == True:
        # ask for tool values
        
        # all cams
        
        allCamsInScript = []
        for n in nuke.allNodes():
            if n.Class() in cameraClasses:
                allCamsInScript.append(n.name())
        allCamsInScript.remove(cam.name()) # remove best camera ...
        allCamsInScript.insert(0,cam.name()) # ... and insert at beginning
        camListPrint = ''
        for c in allCamsInScript:
            camListPrint = camListPrint + c + ' '
        camListPrint = camListPrint[:-1]
        
        #bg, info only. will be determined by selected node - if any ..

        #formatPrint = form

        #panel
        panel = nuke.Panel("C2T")
        panel.addSingleLineInput("label:", card['label'].value())
        panel.addSingleLineInput("range:", str(first)+"-"+str(last))
        panel.addSingleLineInput("ref frame:", str(ref))
        panel.addEnumerationPulldown("camera:", camListPrint)
        #panel.addSingleLineInput("format:", formatPrint)
        if label == '':
            panel.addBooleanCheckBox('reverse label', True)
            
        #panel.show()
        
        if panel.show():
            first = int(panel.value("range:").split("-")[0])
            last = int(panel.value("range:").split("-")[1])
            ref = int(panel.value("ref frame:"))
            cam = nuke.toNode(panel.value("camera:"))
            label = panel.value("label:")
            # reverse label
            if panel.value("reverse label") == True:
                card['label'].setValue(panel.value("label:"))
        else:
            nuke.message('canceled')
            nuke.delete(bg) # clean the mess up
            return
    else:
        print 'no dialog, use auto-created input values'
    
    # labels are usefull!!
    if label == '':
        panel = nuke.Panel("C2T label")
        panel.addSingleLineInput("label:", '')
        panel.addBooleanCheckBox('reverse label', True)
        if panel.show():
            label = panel.value("label:")
            if panel.value("reverse label") == True:
                card['label'].setValue(panel.value("label:"))
            else:
                nuke.message('no label - no roto!')
                nuke.delete(bg) # clean the mess up
                return
        else:
            return
    print '########'
    print 'first', first
    print 'last', last
    print 'ref', ref
    #print 'bg', form
    print 'cam', cam.name()
    print 'card', card.name()
    print 'label', label
    print '########' 
    
    # create master axis and corner slaves
    
    aM = nuke.nodes.Axis2(name = 'aM', xform_order = 3, xpos = x, ypos = y+50)
    uscale = card['uniform_scale'].value()
    scalex = card['scaling'].value(0)
    scaley = card['scaling'].value(1)
    
    if card['translate'].isAnimated() is True:
        aM['translate'].copyAnimations(card['translate'].animations())
    else:
        aM['translate'].setValue(card['translate'].value())
    
    if card['rotate'].isAnimated() is True:
        aM['rotate'].copyAnimations(card['rotate'].animations())
    else:
        aM['rotate'].setValue(card['rotate'].value())
        
        
    # slaves
    a1 = nuke.nodes.Axis2(name = 'a1', xform_order = 1, xpos = x, ypos = y+50)
    a2 = nuke.nodes.Axis2(name = 'a2', xform_order = 1, xpos = x, ypos = y+50)
    a3 = nuke.nodes.Axis2(name = 'a3', xform_order = 1, xpos = x, ypos = y+50)
    a4 = nuke.nodes.Axis2(name = 'a4', xform_order = 1, xpos = x, ypos = y+50)
    
    a1['translate'].setValue([-0.5*uscale*scalex,rootAspect*-0.5*uscale*scaley,0])
    a2['translate'].setValue([0.5*uscale*scalex,rootAspect*-0.5*uscale*scaley,0])
    a3['translate'].setValue([0.5*uscale*scalex,rootAspect*0.5*uscale*scaley,0])
    a4['translate'].setValue([-0.5*uscale*scalex,rootAspect*0.5*uscale*scaley,0])
    
    aL = [a1,a2,a3,a4]
    
    for a in aL:
        a.setInput(0,aM)

    # reconcile
    r1 = nuke.nodes.Reconcile3D(name = 'r1', xpos = x, ypos = y+50)
    r2 = nuke.nodes.Reconcile3D(name = 'r2', xpos = x, ypos = y+50)
    r3 = nuke.nodes.Reconcile3D(name = 'r3', xpos = x, ypos = y+50)
    r4 = nuke.nodes.Reconcile3D(name = 'r4', xpos = x, ypos = y+50)
    
    rL = [r1,r2,r3,r4]
    
    for r in rL:
        r.setInput(2,aL[rL.index(r)])
        r.setInput(1,cam)
        r.setInput(0,bg)
        
    # run with threading
    global stop_event 
    stop_event = threading.Event()
    threading.Thread(target=execRC, kwargs=dict(first=first,last=last)).start() 
    while not stop_event.is_set():
        time.sleep(0.1)
    
    # corner pin normal


    try :
        cp = nuke.nodes.CProject(xpos = x+110, ypos = y)
        cp['camera'].setValue(cam.name())
        cp['translate'].setValue(card['translate'].value())
        cp['rotation'].setValue(card['rotate'].value())
        cp['element'].setValue(label)
        cp['name'].setValue(cp['name'].value().replace('CProject','CP')+"_"+label)
        cp['refFrame'].setValue(str(ref))
    except:
        cp = nuke.nodes.CornerPin2D(label = label +' ('+str(ref)+')', xpos = x+110, ypos = y)  
    cp['to1'].copyAnimations(r1['output'].animations())
    cp['to2'].copyAnimations(r2['output'].animations())
    cp['to3'].copyAnimations(r3['output'].animations())
    cp['to4'].copyAnimations(r4['output'].animations())
    cp['from1'].setValue(r1['output'].getValueAt(ref))
    cp['from2'].setValue(r2['output'].getValueAt(ref))
    cp['from3'].setValue(r3['output'].getValueAt(ref))
    cp['from4'].setValue(r4['output'].getValueAt(ref))

    
    
    
    # corner pin matrix & roto 
    cpm = nuke.nodes.CornerPin2D(label = label+' matrix ('+str(ref)+')', xpos = x+220, ypos = y)   
    roto = nuke.nodes.Roto( xpos = x+330, ypos = y) 
    roto['name'].setValue(roto['name'].value().replace('Roto','R')+"_"+label)
    nuke.show(roto)
    
    roto_transform = roto['curves'].rootLayer.getTransform() # transform of root layer in roto
    cpm['transform_matrix'].setAnimated()
    projectionMatrixTo = nuke.math.Matrix4()
    projectionMatrixFrom = nuke.math.Matrix4()

    frame = first
    while frame<last+1:

        to1x = cp['to1'].valueAt(frame)[0]
        to1y = cp['to1'].valueAt(frame)[1]
        to2x = cp['to2'].valueAt(frame)[0]
        to2y = cp['to2'].valueAt(frame)[1]
        to3x = cp['to3'].valueAt(frame)[0]
        to3y = cp['to3'].valueAt(frame)[1]
        to4x = cp['to4'].valueAt(frame)[0]
        to4y = cp['to4'].valueAt(frame)[1]

        from1x = cp['from1'].valueAt(frame)[0]
        from1y = cp['from1'].valueAt(frame)[1]
        from2x = cp['from2'].valueAt(frame)[0]
        from2y = cp['from2'].valueAt(frame)[1]
        from3x = cp['from3'].valueAt(frame)[0]
        from3y = cp['from3'].valueAt(frame)[1]
        from4x = cp['from4'].valueAt(frame)[0]
        from4y = cp['from4'].valueAt(frame)[1]
    
        projectionMatrixTo.mapUnitSquareToQuad(to1x,to1y,to2x,to2y,to3x,to3y,to4x,to4y)
        projectionMatrixFrom.mapUnitSquareToQuad(from1x,from1y,from2x,from2y,from3x,from3y,from4x,from4y)
        theCornerpinAsMatrix = projectionMatrixTo*projectionMatrixFrom.inverse()
        theCornerpinAsMatrix.transpose()

        for i in range(0,16):
            cpm['transform_matrix'].setValueAt(theCornerpinAsMatrix[i],frame,i)
            
        for i in range(0,16):
            roto_transform.getExtraMatrixAnimCurve(0,i).addKey(frame,cpm['transform_matrix'].getValueAt(frame,i))  
            
        frame = frame + 1

    roto['curves'].changed()
    # check for turnover
    k = cp['to1']
    vals = []
    valSort =[]
    for i in range(first,last+1):
        vals.append(k.valueAt(i,0))
        valSort.append(k.valueAt(i,0))
    valSort.sort()
    min = valSort[0]
    max = valSort[-1]
    warning = ''
    if math.fabs(vals.index(max)-vals.index(min)) == 1:
        warning = 'Warning: perspective problem detected'


    #clean up
    rmL = [r1,r2,r3,r4,a1,a2,a3,a4,aM]
    for i in rmL:
        nuke.delete(i)
    nuke.delete(bg)
    
    if dialog == False:
        roto.setXYpos(x+100,y)
        #remove all non roto nodes
        nuke.delete(cp)
        nuke.delete(cpm)
        
        
    # show warning if any
    if warning != '':
        nuke.message(warning)

    print 'C2T done.'
#TEST
#C2T(True)
