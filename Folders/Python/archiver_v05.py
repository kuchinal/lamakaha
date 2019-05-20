#Nuke Archiver v.04
#Updated July 20, 2009
import nuke
import os
import shutil
from fnmatch import fnmatch
from time import strftime

#Functions
def _archiverPanel(outPath):
	aPanel = nuke.Panel("Archive This Comp")
	aPanel.addFilenameSearch("Output Path:", "/Volumes/Xsan/")
	aPanel.addButton("Cancel")
	aPanel.addButton("OK")

	retVar = aPanel.show()

	outPath[0] = aPanel.value("Output Path:")

	return retVar


def archiveThisComp():
	#variable declarations
	n = nuke.allNodes()

	destPath = None
	seqNameEnds = ('%04d','%03d','%02d','%01d','%d','####','###','##','#')

	archiverParams = {
		'outPath' : ["/Volumes/Xsan/"]}

	#----------------------
	#-----Doin' Stuff------
	#----------------------
	panelResult = _archiverPanel(**archiverParams)

	#If they hit OK
	if panelResult is 1:
		#get panel values and build new local path for footage
		localPath = archiverParams['outPath'][0]

		#check if local directory already exists. Ask to create it if it doesn't
		if not os.path.exists(localPath):
			if nuke.ask("Directory does not exist. Create now?"):
				os.makedirs(localPath)
			else:
				raise Exception, "Not a valid target directory."
			
		#get and strip script name
		scriptName = nuke.Root().name().rpartition('/')[2]
		#save script to archive path
		newScriptPath = localPath + scriptName
		nuke.scriptSaveAs(newScriptPath)

		#create log file and write header info to it
		fOut = open(localPath + 'Archive Log.txt', 'w')
		fOut.write('Comp archived %s at %s\n\n\n' % (strftime("%m/%d/%Y"), strftime("%H:%M:%S")))   
		fOut.write('Comp Name: %s\n\n' % (scriptName, ))
		fOut.write('Files archived to:\n\t%s\n\n\n' % (localPath, ))

		tempCount = 0

		#build lists of Read and ReadGeo nodes
		readNodes = [i for i in n if i.Class() == "Read"]
		readPaths = [node['file'].value() for node in readNodes]
		readGeoNodes = [i for i in n if i.Class() == "ReadGeo2" or i.Class() == "ReadGeo"]
		readGeoPaths = [node['file'].value() for node in readGeoNodes]

		#REMOVE DUPLICATE READ NODES AND REPLACE THEM WITH POSTAGE STAMPS
		dupNodes = []
		for node in readNodes:
			dupSet = []
			if readPaths.count(node['file'].value()) > 1:
				dupSet = [i for i in readNodes if i['file'].value() == node['file'].value()]
				dupNodes.append(dupSet)
				for dup in dupSet:
					readNodes.remove(dup)
					readPaths.remove(dup['file'].value())

		if dupNodes:
			for set in dupNodes:
				set.sort()
				readNodes.append(set[0])
				for count in range(1,len(set)):
					set[count]['selected'].setValue(True)
					pStamp = nuke.nodes.PostageStamp(name = "PStamp_" + set[count].name(), label = set[count].name(), hide_input = True, xpos = set[count].xpos(), ypos = set[count].ypos())
					pStamp.setInput(0,set[0])
					nuke.delete(set[count])

		#process Read nodes
		fOut.write('Read nodes and associated source files:\n')

		for node in readNodes:
			tempCount += 1
			#get Read node's footage path
			netPath = node['file'].value()
			netPathTuple = netPath.rpartition('/')
			#build local path to assign to Read node
			localReadPath = '%sfootage/%s' % (localPath, node.name())
			#create local folder for current Read node
			os.makedirs(localReadPath)
			seqName = netPathTuple[2]
			seqTuple = seqName.rpartition('.')

			#test whether the Read node is reading a sequence or a single file and proceed accordingly
			if seqTuple[0].endswith(seqNameEnds):
				tempCount += 1
				seqPrefixTuple = seqTuple[0].partition(seqTuple[0][-4])
				print "\n\nCopying sequence %d: %s..." % (tempCount, seqName)

				for fileName in os.listdir(netPathTuple[0]):
					if fnmatch(fileName, seqPrefixTuple[0] + '*'):
						shutil.copy2('%s/%s' % (netPathTuple[0], fileName), localReadPath)

			#single file copy script
			else:
				print "\n\nCopying plate: %s..." % (netPath.rpartition('/')[2], )
				try:
					shutil.copy2(netPath, localReadPath)
				except OSError:
					print "...Plate already exists"

			#re-path each Read node to the local footage
			node['file'].setValue('%sfootage/%s/%s' % (localPath, node.name(), seqName))
			#write string containing Read node name followed by file sequence to output file
			fOut.write('\t%s: %s\n' % (node.name(), seqName))

		#process Geometry nodes
		localReadGeoPath = ""
		
		if readGeoNodes:
			fOut.write('\nReadGeo nodes and associated geometry files:\n')
			
			for node in readGeoNodes:
				tempCount += 1
				#get ReadGeo node's geometry path
				netPath = node['file'].value()
				netPathTuple = netPath.rpartition('/')
				#build local path to assign to Read node
				localReadGeoPath = '%sgeometry/%s' % (localPath, node.name())
				#create local folder for current ReadGeo node
				os.makedirs(localReadGeoPath)
				seqGeoName = netPathTuple[2]
				seqGeoTuple = seqGeoName.rpartition('.')
	
				#test whether the ReadGeo node is reading a sequence of obj or a single file and proceed accordingly
				if seqGeoTuple[0].endswith(seqNameEnds):
					tempCount += 1
					seqGeoPrefixTuple = seqGeoTuple[0].partition(seqGeoTuple[0][-4])
					print "\n\nCopying Geometry sequence %d: %s..." % (tempCount, seqGeoName)
	
					for fileName in os.listdir(netPathTuple[0]):
						if fnmatch(fileName, seqGeoPrefixTuple[0] + '*'):
							shutil.copy2('%s/%s' % (netPathTuple[0], fileName), localReadGeoPath)
	
				#single file copy script
				else:
					print "\n\nCopying Geometry: %s..." % (netPath.rpartition('/')[2], )
					try:
						shutil.copy2(netPath, localReadGeoPath)
					except OSError:
						print "...Geometry already exists"
	
				#re-path each Read node to the local footage
				node['file'].setValue('%sgeometry/%s/%s' % (localPath, node.name(), seqGeoName))
				#write string containing ReadGeo node name followed by file sequence to output file
				fOut.write('\t%s: %s\n' % (node.name(), seqGeoName))

		print "Done"

		#write total number of copied files to output file
		fOut.write('\n\n%d files total' % (sum((len(f) for _, _, f in os.walk(localPath)))-2, ))
		fOut.close()
		
		#save script
		nuke.scriptSave()
		nuke.message("Archive complete")

	#CANCEL
	else:
		nuke.message("Canceled by user")