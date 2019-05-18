



def NameScanLineWindows():
    import nuke, os, sys, pyperclip
    plat = sys.platform
    nkFullPath = nuke.Root().knob('name').getValue()
    nkPath, nkName = os.path.split(nkFullPath)
    nkPath += "/"

    Name = nkName.rpartition(".")[0]
    print Name
    m=nuke.menu('Nuke')
    m.addMenu(Name).addCommand('Copy Shot','copy2clip(nuke.Root().name().rpartition("/")[2].rpartition("_")[0])',icon = "my.png")
    m.addMenu(Name).addCommand('Slapcomps','ReadnamesSlapcomp.ReadnamesSlapcomp()',icon = "my.png")    
    
        
def Name():
    import nuke, os, sys, pyperclip
    plat = sys.platform
    nkFullPath = nuke.Root().knob('name').getValue()
    nkPath, nkName = os.path.split(nkFullPath)
    nkPath += "/"
    print nkName


    Name = nkName.rpartition("_2d")[0]
    print Name
    m=nuke.menu('Nuke')
    if plat == "linux2":
        m.addCommand('Shot','pyperclip.copy(nuke.Root().name().rpartition("/")[2].rpartition("_")[0])')
    elif plat == "win32":
        u = m.addMenu(Name)
        u.addCommand('Copy Shot','copy2clip(nuke.Root().name().rpartition("/")[2].rpartition("_")[0])',icon = "my.png")
		
		
def NameBlackSail():
    import nuke
    nkFullPath = nuke.Root().knob('name').getValue()
    Name = nkFullPath.split("/")[7]
    Name = Name.split(".")[0]
    m=nuke.menu('Nuke')
    u = m.addMenu(Name)
    u.addCommand('Copy Shot','copy2clip(nuke.Root().name().rpartition("/")[2].rpartition("_")[0])',icon = "my.png")

def NameBigHug():
    import nuke
    nkFullPath = nuke.Root().knob('name').getValue()
    Name = nkFullPath.split("/")[9]
    Name = Name.split(".")[0]
    m=nuke.menu('Nuke')
    u = m.addMenu(Name)
    print Name

        def NameTrixter():
    import nuke
    nkFullPath = nuke.Root().knob('name').getValue()
    try:
		Name = nkFullPath.split("/")[10]
		Name = Name.split(".")[0]
		Name = Name.rpartition("_")[0]
		Name = "| "+Name.rpartition("S_")[2]+" |"
		m=nuke.menu('Nuke')
		u = m.addMenu(Name)
		print Name
    except:
		print "not matching pattern"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
