

import nuke
def Disabler_Enabler():
  d = nuke.nodes.NoOp(name='Disabler')
  D = nuke.Boolean_Knob("Defocus", "Defocus   ")           
  d.addKnob(D)                                                                                  
  B = nuke.Boolean_Knob("Blur", "Blur   ")           
  d.addKnob(B) 
  Z = nuke.Boolean_Knob("Z_Blur", "Z_Blur   ")           
  d.addKnob(Z) 
  V = nuke.Boolean_Knob("Vector_Blur", "Vector_Blur   ")             
  d.addKnob(V) 
  I = nuke.Boolean_Knob("I_Distort", "I_Distort   ")               
  d.addKnob(I) 
  L = nuke.Boolean_Knob("LightWrap", "LightWrap   ")                 
  d.addKnob(L) 
  G = nuke.Boolean_Knob("Glow", "Glow   ")           
  d.addKnob(G)
  Disabler = nuke.PyScript_Knob("Disabler", "Disabler_Enabler")               
  d.addKnob(Disabler)
  d['Disabler'].setValue('Dica.Dica()')
 

    
