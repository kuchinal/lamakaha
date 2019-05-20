import nuke
import operator
import time
stored = []
def recurseUpSelect(node):
    if node != None and node not in stored:
        node.knob('selected').setValue(True)
        for i in range(node.inputs()):
            recurseUpSelect(node.input(i)) 
            stored.append(node.input(i))


def collectReads():
	try:
		mdNode = nuke.toNode("metadata_TRX")['metadata']
		y = time.time()
		selectedWrites = []
		reads = {}
		meta = ""
		writes = nuke.allNodes('Write')
		for w in writes:#first loop to collect all selected Write nodes
			if w.isSelected():
				selectedWrites.append(w)
				print w['name'].value()

		for one in nuke.allNodes():#deselect all nodes
			one.setSelected(False)

		for w in writes:#second loop to find all Read nodes
			t = time.time()
			recurseUpSelect(w)
			element = w['wm_layer'].value()
			name = w['name'].value()
			if element == "":
				element = "beauty"
			if w in selectedWrites:
				element=element+"(Selected)"
			fullName = name+"_"+element
			print fullName
			for one in nuke.selectedNodes():
				if "Read" in one.Class() or "Render_Input_CG" in one['name'].value():
					version = one['file'].value()
					count = 1
					for dude in reads:
						if reads[dude] == fullName:
							fullName == fullName+str(count)
							count = count+1

					reads[version]=fullName
				one.setSelected(False)
			for one in nuke.allNodes():#deselect all nodes
				one.setSelected(False)
			print "________________________________________________________"
			print name
			print "read collect: "+str(time.time()-t)


		for w in selectedWrites:
			w.setSelected(True)

		readsSorted = sorted(reads.items(), key=operator.itemgetter(1))
		for one in readsSorted:
			meta = meta+"{set "+one[0].replace(" ","_")+" "+one[1]+"}\n"

		mdNode.fromScript(meta)
		print "------------------"
		print "read collect: "+str(time.time()-y)
	except:
		print "no Modify Metadata node found, no metadata will be ingested"



