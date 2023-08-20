def DotsHst(type):
	import nuke
	dotscale = nuke.toNode("preferences")['dot_node_scale'].value()
	dotS = 12*dotscale/2

	if type == 'transSel' or type == 'newDown':
		if type == 'newDown':
			n = nuke.createNode('Dot')
		else:
			n = nuke.selectedNode()
		try:
			u = n.input(0)
			for i in nuke.allNodes():
				if n in i.dependencies(nuke.INPUTS):
					d = i
					break

			uX, uY = u.xpos() + u.screenWidth()/2 , u.ypos() + u.screenHeight()/2
			#nX, nY = n.xpos() + n.screenWidth()/2 , n.ypos() + n.screenHeight()/2
			dX, dY = d.xpos() + d.screenWidth()/2 , d.ypos() + d.screenHeight()/2 

			if uX == dX:
				n['xpos'].setValue(int(uX - dotS))
			else:
				n.setXYpos(int(uX - dotS), int(dY - dotS))
		except:
			print ''
	
	if type == 'allUp':
		try:
			n = nuke.selectedNode()           
			uli = n.dependencies(nuke.INPUTS)
			nX, nY = n.xpos() + n.screenWidth()/2 , n.ypos() + n.screenHeight()/2

			for u in uli:
				uX, uY = u.xpos() + u.screenWidth()/2 , u.ypos() + u.screenHeight()/2

				if uX != nX and uY != nY:
					index = uli.index(u)
					u.setSelected(True)
					u.selectOnly()
					d = nuke.createNode('Dot')
					if index == 0:
						d.setXYpos(int(nX - dotS), int(uY - dotS))                 
					else:
						d.setXYpos(int(uX - dotS), int(nY - dotS))

			n.setSelected(True) 

		except:
			print ''
	
	if type == 'label':
		q = nuke.getInput("Description")
		if q:
			try:
				q = q.replace(' ', '_')
				n = nuke.selectedNode()
				nX, nY = n.xpos(), n.ypos() 
				d = nuke.nodes.Dot(label = q, note_font_size = 20, tile_color = 4000)
				
				#place
				endnode = True
				for i in nuke.allNodes():
					if n in i.dependencies(nuke.INPUTS) and 'Viewer' not in i.Class():
						print i.name()
						endnode = False
						break
				if endnode == True:
					d.setXYpos(int(nX+n.screenWidth()/2-dotS), nY+100)
				else:
					d.setXYpos(nX+100, nY+100)

				d.setInput(0,n)
			except:
				print ''
