def inn():
	import nuke
	n=nuke.selectedNode()
	n['operation'].setValue('mask')
	n['bbox'].setValue('A')