import nuke
def Dica():
      d = nuke.selectedNode()
      D=d['Defocus'].value()
      B=d['Blur'].value()
      Z=d['Z_Blur'].value()
      V=d['Vector_Blur'].value()
      I=d['I_Distort'].value()
      L=d['LightWrap'].value()
      G=d['Glow'].value()
    
    
      DD = nuke.allNodes("Defocus")
      BB = nuke.allNodes("Blur")
      ZZ = nuke.allNodes("ZBlur")
      VV = nuke.allNodes("VectorBlur")
      II = nuke.allNodes("IDistort")
      LL = nuke.allNodes("LightWrap")
      GG = nuke.allNodes("Glow")
      
    
    
      if D is True:
        for i in DD:
          i['disable'].setValue(1)
      else:
        for i in DD:
          i['disable'].setValue(0)
    
    
      if B is True:
        for i in BB:
          i['disable'].setValue(1)
      else:
        for i in BB:
          i['disable'].setValue(0)
    
      if Z is True:
        for i in ZZ:
          i['disable'].setValue(1)
      else:
        for i in ZZ:
          i['disable'].setValue(0)
    
      if V is True:
        for i in VV:
          i['disable'].setValue(1)
      else:
        for i in VV:
          i['disable'].setValue(0)
    
      if I is True:
        for i in II:
          i['disable'].setValue(1)
      else:
        for i in II:
          i['disable'].setValue(0)
    
      if L is True:
        for i in LL:
          i['disable'].setValue(1)
      else:
        for i in LL:
          i['disable'].setValue(0)
    
      if G is True:
        for i in GG:
          i['disable'].setValue(1)
      else:
        for i in GG:
          i['disable'].setValue(0)