import nuke
def Baker():  
    lastFrame=nuke.root().knob('last_frame').value()+1
    cam = nuke.selectedNode()
    camb = nuke.createNode("Camera2")
    foc = cam['focal'].getValue()
    focb = camb['focal'].setValue(foc)
    camb.setInput(0,None)
    camb['tile_color'].setValue(4294901760L)
    camb['gl_color'].setValue(4294901760L)
    camb['label'].setValue('Baked')
    camb['tile_color'].setValue(4294901760L)
    #camb['icon'].setValue('Baker.png')
    x = cam.xpos()
    y = cam.ypos()
    camb.setXYpos(x,y+100)


    hap = cam['haperture'].getValue()
    hapb = camb['haperture'].setValue(hap)
    vap = cam['vaperture'].getValue()
    vapb = camb['vaperture'].setValue(vap)


    win = cam['win_translate'].getValue()
    winb = camb['win_translate'].setValue(win)
    fin = cam['win_scale'].getValue()
    finb = camb['win_scale'].setValue(fin)
    camb['translate'].setAnimated()
    camb['rotate'].setAnimated()
    frame = 0
    while frame < lastFrame:
      posx = cam['translate'].valueAt(frame,0)
      posy = cam['translate'].valueAt(frame,1)
      posz = cam['translate'].valueAt(frame,2)
      posbx = camb['translate'].setValueAt(posx,frame,0)
      posby = camb['translate'].setValueAt(posy,frame,1)
      posbz = camb['translate'].setValueAt(posz,frame,2)
      rotx = cam['rotate'].valueAt(frame,0)
      roty = cam['rotate'].valueAt(frame,1)
      rotz = cam['rotate'].valueAt(frame,2)
      rotbx = camb['rotate'].setValueAt(rotx,frame,0)
      rotby = camb['rotate'].setValueAt(roty,frame,1)
      rotbz = camb['rotate'].setValueAt(rotz,frame,2)
      frame = frame+1

