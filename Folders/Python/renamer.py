import nuke

def renamer():
  n = nuke.selectedNodes("Read")
  for node in n:
    name = node['file'].value()
    refl = name.find('refl')
    refr = name.find('refr')
    gi = name.find('global')
    Shad = name.find('shad')
    diff = name.find('diff')
    occlu = name.find('occlu')
    rgb = name.find('rgb')
    spec = name.find('spec')
    light = name.find('light')
    zdepth = name.find('depth')
    velo = name.find('velocity')
    norm = name.find('normal')
    alpha = name.find('alpha')
    multi = name.find('multi')
    beauty = name.find('beauty')
    color = name.find('color')
  
    if refl>0:
     node['name'].setValue('REFLECT')
    if refr>0:
     node['name'].setValue('REFRACT')
    if gi>0:
     node['name'].setValue('GI')
    if Shad>0:
     node['name'].setValue('SHADOW')
    if diff>0:
     node['name'].setValue('DIFFUS')
    if occlu>0:
     node['name'].setValue('OCCLUS')
    if rgb>0:
     node['name'].setValue('RGB')
    if spec>0:
     node['name'].setValue('SPECULAR')
    if light>0:
     node['name'].setValue('LIGHT')
    if zdepth>0:
     node['name'].setValue('DEPTH')
    if velo>0:
     node['name'].setValue('VELOCITY')
    if norm>0:
     node['name'].setValue('NORMALS')
    if alpha>0:
     node['name'].setValue('ALPHA')
    if multi>0:
     node['name'].setValue('MULTI')
    if beauty>0:
     node['name'].setValue('BEAUTY')
    if color>0:
     node['name'].setValue('COLOR')
  
  
   





