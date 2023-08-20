import nuke
import nukescripts

def getReadFromWrite():
	#WriteNodes = [node for node in nuke.selectedNodes() if node.Class()=='Write']
	count = 1
	while nuke.exists('AutoWrite' + str(count)):
		count += 1
	for node in nuke.selectedNodes():
		#rfirst = int(node['first'].value())
		#rlast = int(node['last'].value())
		readNode = nuke.createNode('Read')
		readNode['file'].setValue(node['file'].getValue())
		readNode['xpos'].setValue(node['xpos'].getValue())
		readNode['ypos'].setValue(node['ypos'].getValue()+100)
		rfirst = nuke.root().knob('first_frame').value()
		rlast = nuke.root().knob('last_frame').value()
		readNode['first'].setValue(rfirst)
		readNode['last'].setValue(rlast)
		#readNode.knob('name').setValue('AutoRead' + str(count))
		#readNode.knob('reload').execute()