def over():
    import nuke
    n=nuke.selectedNodes()
    for n in n:
      if "Deep" in n['name'].value():
        n['operation'].setValue('combine')
      else:
        n['operation'].setValue('over')
  
def plus():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
      if "Merge" in n.Class():
        n['operation'].setValue('plus')


  
def ccopy():
  import nuke 
  n=nuke.selectedNodes()
  for n in n:
      if "Merge" in n.Class():
          n['operation'].setValue('copy')
          n['bbox'].setValue("A")

def atop():
  import nuke 
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('atop')
      n['bbox'].setValue("B")

  
def minus():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('minus')
      n['bbox'].setValue("B")

  
def under():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('under')

  
def divide():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('divide')
  
def disjoint():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('disjoint-over')

  
def multiply():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('multiply')

  
def fromm():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('from')


  
def inn():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('mask')


    
def out():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      if "Deep" in n['name'].value():
        n['operation'].setValue('holdout')
      else:
        n['operation'].setValue('stencil')



def screen():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('screen')

  
def xor():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('max')

def xorm():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('min')

def aver():
  import nuke
  n=nuke.selectedNodes()
  for n in n:
    if "Merge" in n.Class():
      n['operation'].setValue('average')  
      

      
      
