
import sys	
import os
import subprocess 
# "a" is an argument yo defined in the function (test.py a)
a = sys.argv[1]
b = a.rpartition("_")[0]
nuke = "/usr/local/Nuke8.0v4/Nuke8.0"
# good example for usage of % sign
path = "/NAS/001_PROJEKTE/22_CREED/04_Production/%s/%s/Comp/Nuke/" %(b,a)
content=os.listdir(path)
low = 0
for item in content:
    if "comp_v" in item and "autosave" not in item and "~" not in item and item.count("_") == 4:
        version = int(item.rpartition('_')[2].rpartition('.')[0].rpartition('v')[2])
        if version > low:
            low = version
low =  "%03d" % low
script = "%s%s_comp_v%s.nk" %(path,a,low)
subprocess.call([nuke, "-V2", script])







