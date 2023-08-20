def cropTobbox(): 
	import nuke
	d = nuke.selectedNode()
	x=d.bbox().x()
	y=d.bbox().y()
	t=d.bbox().w()+d.bbox().x()
	r=d.bbox().h()+d.bbox().y()
	crop = nuke.createNode("Crop")
	crop['box'].setValue([x,y,t,r])
	crop['reformat'].setValue(1)
	trans = nuke.createNode("Transform")
	trans['translate'].setValue([x,y])