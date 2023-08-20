
import os
import nuke
import sys


def Win():
    import os
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b)[0]
    u = os.path.normpath(u)
    print u
    cmd = 'explorer "%s"' % (u)
    print cmd
    os.system(cmd) 


def Linux(): 
	import os 
	import subprocess 
	a=nuke.selectedNode() 
	b=a['file'].value() 
	u=os.path.split(b) [0] 
	u = os.path.normpath (u) 
	print u 
	subprocess.Popen(['nautilus','%s' % (u)])
	
def LinuxJPEG(): 
    import os 
    import subprocess 
    a=nuke.selectedNode() 
    b=a['file'].value() 
    u=os.path.split(b) [0] 
    u = os.path.normpath (u) 

    fullpath = u 
    fullpath = fullpath.replace("exr","jpg")
    fullpath = fullpath.replace("elin","jflut")



    u = fullpath
    print u 

    subprocess.Popen(['nautilus','%s' % (u)])



def Mac():
    import os
    import subprocess
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b) [0]
    u = os.path.normpath (u)
    print u
    subprocess.Popen(['open', '-R', '%s' % (u)])



def Explorer():
    plat = sys.platform
    if plat == "darwin":
        Mac()
    elif plat == "linux2":
        Linux()
    elif plat == "win32":
        Win()


def Win():
    import os
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b)[0]
    u = os.path.normpath(u)
    fullpath=u
    fullpath = fullpath.replace("exr",'jpg')
    fullpath = fullpath.replace("linear_odd",'proxy_odd')
    cmd = 'explorer "%s"' % (fullpath)
    print cmd
    os.system(cmd) 

    
def ExplorerJPEG():
    plat = sys.platform
    if plat == "darwin":
        Mac()
    elif plat == "linux2":
        LinuxJPEG()
    elif plat == "win32":
        Win()
