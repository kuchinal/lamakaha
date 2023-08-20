
1. Copy the folder "eTools" in your .nuke folder (under C:/Users/...)

2. Add the following lines to your init.py file (right click and edit ) :

	nuke.pluginAddPath('./eTools')

	nuke.pluginAddPath('./eTools/Icons')
	nuke.pluginAddPath('./eTools/Gizmos')


3. Add the following lines to your menu.py file (right click and edit ) :

	toolbar = nuke.menu('Nodes')
	eMenu = toolbar.addMenu('eTools', icon='eTools.png')
	eMenu.addCommand('eSmartReformat', 'nuke.createNode("eSmartReformat")', icon='eSmartReformat.png')

	PS. If you have already copied those lines while installing my prevoius gizmo "eFibonacciGlow", just copy the last one.


4. Please share and visit my website: ermesvincenti.wordpress.com