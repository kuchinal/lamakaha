

import nuke
def LuxxRenamer():
  n = nuke.selectedNodes()
  for n in n:
   string = n['file'].value()
   Basic = string.find("RGB")
   Atmosphere = string.find("Atmosphere")
   GI = string.find("Global")
   Lighting = string.find("Lighting")
   TotalLighting = string.find("TotalLighting")
   Reflection = string.find("Reflection")
   Refraction = string.find("Refraction")
   ID = string.find("ID")
   Shadows = string.find("Shadows")
   Specular = string.find("Specular")
   Wire = string.find("Wire")
   ZDepth = string.find("ZDepth")
   Alpha = string.find("Alpha")
   MultiMatte = string.find("MultiMatte")
   MatteShadow = string.find("MatteShadow")
   Normals = string.find("Normals")
   BumpNormals= string.find("BumpNormals")
   DiffuseFilter= string.find("DiffuseFilter") 
   Illuminance= string.find("Illuminance") 

 
 
   if Basic>0:
     n['label'].setValue('Beauty')
   if Basic>0:
     n['name'].setValue('Basic')

   if Atmosphere>0:
     n['label'].setValue('Atmosphere')
   if GI>0:
     n['label'].setValue('GI')
   if Lighting>0:
     n['label'].setValue('Lighting')
   if TotalLighting >0:
     n['label'].setValue('TotalLighting ')

   if Reflection>0:
     n['label'].setValue('Reflection')
   if Refraction>0:
     n['label'].setValue('Refraction')
   if ID>0:
     n['label'].setValue('ID')
   if Shadows>0:
     n['label'].setValue('Shadows')
   if Specular>0:
     n['label'].setValue('Specular')
   if Wire>0:
     n['label'].setValue('Wire')
   if ZDepth>0:
     n['label'].setValue('ZDepth')
   if Alpha>0:
     n['label'].setValue('Alpha')
   if MultiMatte>0:
     n['label'].setValue('MultiMatte')
   if MatteShadow>0:
     n['label'].setValue('MatteShadow')
   if Normals>0:
     n['label'].setValue('Normals')
   if BumpNormals>0:
     n['label'].setValue('BumpNormals')
   if DiffuseFilter>0:
     n['label'].setValue('DiffuseFilter')
   if Illuminance>0:
     n['label'].setValue('Illuminance')


 