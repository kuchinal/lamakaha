
#select all yours transforms and run this ImpactScale()
def ImpactScale():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
      lastFrame=nuke.root().knob('last_frame').value()+1
      frame = 1001
      while frame<lastFrame:
        flashing = n['scaling'].getValueAt(frame,0)
        lashing = n['scaling'].getValueAt(frame-1,0)
        if flashing>50 and lashing<50:
            n['label'].setValue(str(frame))
        frame = frame+1

        
        
# select all your particles and run setFirstFrame()      
def setFirstFrame():
    n = nuke.selectedNodes()
    for node in n:
        t = node.dependencies(nuke.INPUTS)[0]
        Frame = int(t['label'].value())
        node['dustHit_startFrame'].setValue(Frame)        
setFirstFrame()




select all transforms and run this for animation
def Erodes():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    framme = int(n['label'].value())
    frammeMid = framme + 3
    frammeEnd = framme + 30
    print framme
    b = n.dependencies(nuke.INPUTS)[0]
    c = b.dependencies(nuke.INPUTS)[0]
    erode = c.dependencies(nuke.INPUTS)[0]
    print erode['name'].value()
    erode['size'].setAnimated()
    erode['size'].setValueAt(100,framme)
    erode['size'].setValueAt(-5,frammeMid)
    erode['size'].setValueAt(100,frammeEnd)
Erodes()



# adjustment of lighting

def Bilick():
  import nuke




Before = thisNode.Before
Before_size = thisNode.Before_size
Before_gain = thisNode.Before_gain
Start = thisNode.Start
Start_size = thisNode.Start_size
Start_gain =thisNode.Start_gain

Hit_size = thisNode.Hit_size
Hit_gain =thisNode.Hit_gain

End =  thisNode.End
End_size = thisNode.End_size
End_gain = thisNode.End_gain

After = thisNode.After
After_size = thisNode.After_size
After_gain = thisNode.After_gain

  n=nuke.selectedNodes()
  for n in n:
    b = n.dependencies(nuke.INPUTS)[0]
    framme = int(b['label'].value())

    frammeBefore = framme - 5
    frammeStart = framme - 3
    frammeEnd = framme + 1
    frammeStop = framme + 5

    n['sm_s'].setAnimated()
    n['multiply'].setAnimated()

    n['sm_s'].setValueAt(3000,frammeBefore)
    n['multiply'].setValueAt(0,frammeBefore)

    n['sm_s'].setValueAt(1000,frammeStart)
    n['multiply'].setValueAt(0.2,frammeStart)

    n['sm_s'].setValueAt(50,framme)
    n['multiply'].setValueAt(1,framme)

    n['sm_s'].setValueAt(1000,frammeEnd)
    n['multiply'].setValueAt(.3,frammeEnd)


    n['sm_s'].setValueAt(300,frammeStop)
    n['multiply'].setValueAt(0,frammeStop)

    n['label'].setValue(str(framme))

Bilick()