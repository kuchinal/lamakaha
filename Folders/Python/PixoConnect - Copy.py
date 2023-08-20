def PixoConnect():
    import nuke
    n = nuke.selectedNodes()
    for node in n:  #defining reads
        if node.Class()== "Read":
            name = node['file'].value()
            dots=name.count(".")
            if dots==2:
                Beauty = node 
            if "Alpha" in name:
                Alpha = node                 
            if "ao" in name:
                ao = node
            if "diffuse" in name:
                diffuse = node
            if "GI" in name:
                GI = node
            if "rawGi" in name:
                rawGi = node            
            if "lighting" in name:
                lighting = node
            if "nrmWorld" in name:
                nrmWorld = node
            if "pntWorld" in name:
                pntWorld = node
            if "rawGI" in name:
                rawGI = node
            if "rawLighting" in name:
                rawLighting = node
            if "rawReflect" in name:
                rawReflect = node
            if "reflect." in name:
                reflect = node
            if "reflectFilter" in name:
                reflectFilter = node
            if "rawShadow" in name:
                rawShadow = node
            if "shadow" in name:
                shadow = node
            if "specular" in name:
                specular = node
            if "SSS" in name:
                sss = node
            if "velocity" in name:
                velocity = node                                                                                                                                                                                    
            if "zDepth" in name:
                zDepth = node
            if "selfIllum" in name:
                selfIllum = node
            if "refract." in name:
                refract = node
            if "refractFilter" in name:
                refractFilter = node            
    for node in n:  #defining NoOps
        if node.Class()== "NoOp":
            name = node['name'].value()
            if "BEAUTY" in name:
                try:
                    node.setInput(0,Beauty)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)        
                
            if "ALPHA" in name:
                try:
                    node.setInput(0,Alpha)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "SSS" in name:
                try:
                    node.setInput(0,sss)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "SELF_ILLUM" in name:
                try:
                    node.setInput(0,selfIllum)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "SPEC" in name:
                try:
                    node.setInput(0,specular)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "REFl" in name:
                try:
                    node.setInput(0,reflect)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "REFL_FILTER" in name:
                try:
                    node.setInput(0,reflectFilter)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "REFRACT" in name:
                try:
                    node.setInput(0,refract)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "REFRA_FILTER" in name:
                try:
                    node.setInput(0,refractFilter)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "RAW_SHADOw" in name:
                try:
                    node.setInput(0,rawShadow)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "RAW_LIGHTINg" in name:
                try:
                    node.setInput(0,rawLighting)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "SHADOW" in name:
                try:
                    node.setInput(0,shadow)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "LIGHTING" in name:
                try:
                    node.setInput(0,lighting)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)
                            
            if "Gi" in name:           
                try:
                    node.setInput(0,GI)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)            
            if "RAW_GI" in name:
                try:
                    node.setInput(0,rawGi)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)  
                
            if "DIFFUSE_FILTER" in name: 
                try:
                    node.setInput(0,diffuse)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)         
                            
            if "zdept" in name:
                try:
                    node.setInput(0,zDepth)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)        
                            
            if "Velocity" in name:
                try:
                    node.setInput(0,velocity)
                except:
                    node['label'].setValue("Not avalaible")
                    node['note_font_size'].setValue(20)
                    node['tile_color'].setValue(4278190335)        
                            
            
          
                
                
                
                
                
                
                
                