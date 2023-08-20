def RV():
    import nuke
    import os
    import nukescripts
    n = nuke.selectedNode()
    try:
        path = n['file'].value()
        path = path.rpartition("/")[0]
        file=os.listdir(path)[5]
        print file
        fullpath = path + "/" + file
        fullpath = fullpath.replace("/",'\\')
        fullpath = fullpath.replace("exr",'jpg')
        fullpath = fullpath.replace("linear_2khd",'proxy_2khd')
        print fullpath
        nukescripts.start(fullpath)
    except:
        nuke.message("Dude!!!! there is nothing in!!!! we all gonna die!!!!")        
# rv at scanline linux pipeline jpeg review  
def RVTrixtersasa():
    import nuke
    import os
    import nukescripts
    dicts={"BROWSER":"/corky/projects/Sputnik_343196/bin/centos-6_x86-64/rv"}
    os.environ.update(dicts)
    n = nuke.selectedNode()
    try:
        path = n['file'].value()
        path = path.rpartition("/")[0]
        file=os.listdir(path)[5]
        fullpath = path + "/" + file
        fullpath = fullpath.replace("exr","jpg")
        fullpath = fullpath.replace("elin","jflut")
        #fullpath = fullpath.replace("main","avid")
        if "whoami" in fullpath:
            #fullpath = fullpath.replace("2048x1536","1920x1080")
            fullpath = fullpath.replace("avid","main")
        if "spides" in fullpath:
            fullpath = fullpath.replace("3840x2160","1920x1080")
        nukescripts.start(fullpath)
        dicts={"BROWSER":"firefox"}
        os.environ.update(dicts)
    except:
        nuke.message("Dude!!!! there is nothing in!!!! we all gonna die!!!!")          
    
# rv at scanline linux pipeline exr review  
def RVTrixterBKP():
    import nuke
    import os
    import nukescripts
    dicts={"BROWSER":"/corky/projects/Sputnik_343196/bin/centos-6_x86-64/rv"}
    os.environ.update(dicts)
    n = nuke.selectedNode()
    try:
        path = n['file'].value()
        path = path.rpartition("/")[0]
        file=os.listdir(path)[5]
        print file
        fullpath = path + "/" + file
        print fullpath
        nukescripts.start(fullpath)
        dicts={"BROWSER":"firefox"}
        os.environ.update(dicts)
    except:
        nuke.message("Dude!!!! there is nothing in!!!! we all gonna die!!!!")   
        
        
        
def RVTrixter():
    import nuke
    import os
    import subprocess
    rv = "/corky/projects/Sputnik_343196/bin/centos-6_x86-64/rv"
    a = nuke.selectedNodes()
    l = []
    for n in a:
        path = n['file'].value()
        l.append(path)
    cmd = [rv]+l
    

    subprocess.Popen(cmd)

def RVcompare():
    import nuke
    import os
    import subprocess
    rv = "/corky/projects/Sputnik_343196/bin/centos-6_x86-64/rv"
    path = nuke.selectedNode()['file'].value()
    ver = path.split("_")[5]
    shot = path.split("_")[3]
    seq = path.split("_")[2]
    ref = path.rpartition("versions")[0]+"versions/S_"+seq+"_"+shot+"_comp_v001_beauty/output/S_"+seq+"_"+shot+"_comp_v001_beauty.%04d.exr"
    l = []
    l.append(path)
    l.append(ref)
    cmd = [rv]+l
    subprocess.Popen(cmd)

    
    
    
def RVwindowsEXR():
    import nuke
    import os
    import nukescripts
    n = nuke.selectedNode()
    path = n['file'].value()
    path = path.rpartition("/")[0]
    file=os.listdir(path)[5]
    fullpath = path + "/" + file
    fullpath = fullpath.replace("/",'\\')
    print fullpath
    nukescripts.start(fullpath)
    
def RVwindowsJpeg():
    import nuke
    import os
    import nukescripts
    n = nuke.selectedNode()
    path = n['file'].value()
    path = path.rpartition("/")[0]
    file=os.listdir(path)[5]
    print file
    fullpath = path + "/" + file
    fullpath = fullpath.replace("/",'\\')
    fullpath = fullpath.replace("exr",'jpg')
    fullpath = fullpath.replace("linear",'proxy')
    print fullpath
    nukescripts.start(fullpath)

