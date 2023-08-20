# Footage_Converter 1.0
#
# A script which converts footage in nuke.
# (C) Copyright: Adrian Heinzel ( adrian.heinzel@rtt.ag ) 2010-09-09


import nuke
import os
import subprocess
import string
import time

def FootageConverter():
	imageWidth = 0
	imageHeight = 0

	for n in nuke.allNodes():
		if n.Class() == "Read":
			imageWidth = n.width()
			imageHeight = n.height()

	class dialog ( object ):
		window = nuke.Panel("Footage Converter")
		window.addEnumerationPulldown("File Format:", "exr jpeg png tiff")
		window.addEnumerationPulldown("Render to:", "SameFolder CreateSubfolder")
		window.addBooleanCheckBox("Reformat?", "0 1")
		window.addSingleLineInput("Image Width:", imageWidth)
		window.addSingleLineInput("Image Height:", imageHeight)
		window.addSingleLineInput("Divide by:", 1)
		window.addSingleLineInput("Percent:", 100)
		window.addEnumerationPulldown("Reformat Filter:", "Cubic Impulse Keys Simon Rifman Mitchell Parzen Notch")
		window.addBooleanCheckBox("Selected Nodes Only", "0 1")
		
	dialogResult = dialog.window.show()
	
	if dialogResult == 1:
		nuke.tprint("Running FootageConvert Script")
	else:
		nuke.tprint("Canceled")
		return None

	if dialog.window.value("Reformat?") == 1:
		
		if imageWidth == dialog.window.value("Image Width:") or imageHeight == dialog.window.value("Image Height:"):
			nuke.tprint("")
		else:
			newWidth = dialog.window.value("Image Width:")
			newHeight = dialog.window.value("Image Height:")
			
		if dialog.window.value("Divide by:") == "1":
			nuke.tprint("")
		else:
			newWidth = int(imageWidth / int(dialog.window.value("Divide by:")))
			newHeight = int(imageHeight / int(dialog.window.value("Divide by:")))
			
		if dialog.window.value("Percent:") == "100":
			nuke.tprint("")
		else:
			newWidth = int(imageWidth * int(dialog.window.value("Percent:")) / 100)
			newHeight = int(imageHeight * int(dialog.window.value("Percent:")) / 100)

	class exr ( object ):
		window = nuke.Panel("EXR Options")
		window.addEnumerationPulldown("Data Type:", "16_Bit_Half 32_Bit_Float")
		window.addEnumerationPulldown("Compression:", "Zip_1_Scanline Zip_16_Scanlines PIZ_Wavelet_32_Scanlines RLE B44 None")
		
	class jpeg ( object ):
		window = nuke.Panel("JPEG Options")
		window.addSingleLineInput("Quality:", 100)
		
	class png ( object ):
		window = nuke.Panel("PNG Options")
		window.addEnumerationPulldown("Data Type:", "8_Bit 16_Bit")
		
	class tiff ( object ):
		window = nuke.Panel("TIFF Options")
		window.addEnumerationPulldown("Data Type:", "8_Bit 16_Bit 32_Bit_Float")
		window.addEnumerationPulldown("Compression:", "Deflate LZW PackBits None")
		
	if dialog.window.value("File Format:") == "exr":
		formatResult = exr.window.show()
		
	if dialog.window.value("File Format:") == "jpeg":
		formatResult = jpeg.window.show()
		
	if dialog.window.value("File Format:") == "png":
		formatResult = png.window.show()
		
	if dialog.window.value("File Format:") == "tiff":
		formatResult = tiff.window.show()
		
	if formatResult == 1:
		nuke.tprint("")
	else:
		nuke.tprint("Canceled")
		return None
		
	if dialog.window.value("Selected Nodes Only") == 1:
		for n in nuke.selectedNodes():
			if n.Class() == "Read":
				nodeYPos = n.ypos()
				nodeXPos = n.xpos()
				
				readFile = n.knob('file').getValue()
				
				tempPath = readFile.split('/')
				newPath = ""
				
				for i in range(0, len(tempPath) - 1):
					newPath += tempPath[i] + "/"
					
				if dialog.window.value("Render to:") == "SameFolder":
					newPath = newPath
					if dialog.window.value("Reformat?") == 1:
						newPath += "_reformat/"
						try:
							os.mkdir(newPath)
						except:
							nuke.tprint("Render Folder already exists!")
				else:
					newPath += "_%s/" % (dialog.window.value("File Format:"))
					try:
						os.mkdir(newPath)
					except:
						nuke.tprint("Render Folder already exists!")
					
				fileName = readFile.split('/')[ - 1]
				fileNameTable = fileName.split('.')
				newFileName = ""
				
				for i in range(0, len(fileNameTable) -1):
					newFileName += fileNameTable[i] + "."
					
				newPath += newFileName
				
				if dialog.window.value("File Format:") == "exr":
					newPath += "exr"
				if dialog.window.value("File Format:") == "jpeg":
					newPath += "jpg"
				if dialog.window.value("File Format:") == "png":
					newPath += "png"
				if dialog.window.value("File Format:") == "tiff":
					newPath += "tif"
				
				if dialog.window.value("Reformat?") == 1:
					reformat = nuke.createNode("Reformat")
					nuke.extractSelected()
					reformat.knob('xpos').setValue(nodeXPos)
					reformat.knob('ypos').setValue(nodeYPos + 150)
					reformat.knob('filter').setValue(dialog.window.value("Reformat Filter:"))
					
					print newWidth
					print newHeight
					
					reformat.knob('type').setValue("to box")
					reformat.knob('box_fixed').setValue(1)
					reformat.knob('box_width').setValue(int(newWidth))
					reformat.knob('box_height').setValue(int(newHeight))
					
					write = nuke.createNode("Write")
					nuke.extractSelected()
					write.knob('xpos').setValue(nodeXPos)
					write.knob('ypos').setValue(nodeYPos + 300)
					
					reformat.setInput(0, n)
					write.setInput(0, reformat)
				else:
					write = nuke.createNode("Write")
					nuke.extractSelected()
					write.knob('xpos').setValue(nodeXPos)
					write.knob('ypos').setValue(nodeYPos + 150)
					
					write.setInput(0, n)
					
				write.knob('file').setValue(newPath)
				write.knob('file_type').setValue(dialog.window.value("File Format:"))
				
				if dialog.window.value("File Format:") == "exr":
					if exr.window.value("Data Type:") == "16_Bit_Half":
						write.knob('datatype').setValue("16 bit half")
					if exr.window.value("Data Type:") == "32_Bit_Float":
						write.knob('datatype').setValue("32 bit float")
					
					if exr.window.value("Compression:") == "Zip_1_Scanline":
						write.knob('compression').setValue("Zip (1 scanline)")
					if exr.window.value("Compression:") == "Zip_16_Scanlines":
						write.knob('compression').setValue("Zip (16 scanlines)")
					if exr.window.value("Compression:") == "PIZ_Wavelet_32_Scanlines":
						write.knob('compression').setValue("PIZ Wavelet (32 scanlines)")
					if exr.window.value("Compression:") == "RLE":
						write.knob('compression').setValue("RLE")
					if exr.window.value("Compression:") == "B44":
						write.knob('compression').setValue("B44")
					if exr.window.value("Compression:") == "None":
						write.knob('compression').setValue("none")
					
				if dialog.window.value("File Format:") == "jpeg":
					write.knob('_jpeg_quality').setValue(float(jpeg.window.value("Quality:")) / 100)
					
				if dialog.window.value("File Format:") == "png":
					if png.window.value("Data Type:") == "8_Bit":
						write.knob('datatype').setValue("8 bit")
					if png.window.value("Data_Type:") == "16_Bit":
						write.knob('datatype').setValue("16 bit")
					
				if dialog.window.value("File Format:") == "tiff":
					if tiff.window.value("Data Type:") == "8_Bit":
						write.knob('datatype').setValue("8 bit")
					if tiff.window.value("Data Type:") == "16_Bit":
						write.knob('datatype').setValue("16 bit")
					if tiff.window.value("Data Type:") == "32_Bit_Float":
						write.knob('datatype').setValue("32 bit float")
						
					if tiff.window.value("Compression:") == "Deflate":
						write.knob('compression').setValue("Deflate")
					if tiff.window.value("Compression:") == "LZW":
						write.knob('compression').setValue("LZW")
					if tiff.window.value("Compression:") == "PackBits":
						write.knob('compression').setValue("PackBits")
					if tiff.window.value("Compression:") == "None":
						write.knob('compression').setValue("none")
						
				n.knob('proxy').setValue(newPath)
	else:
		for n in nuke.allNodes():
			if n.Class() == "Read":
				nodeYPos = n.ypos()
				nodeXPos = n.xpos()
				
				readFile = n.knob('file').getValue()
				
				tempPath = readFile.split('/')
				newPath = ""
				
				for i in range(0, len(tempPath) - 1):
					newPath += tempPath[i] + "/"
					
				if dialog.window.value("Render to:") == "SameFolder":
					newPath = newPath
				else:
					newPath += "_%s/" % (dialog.window.value("File Format:"))
					try:
						os.mkdir(newPath)
					except:
						nuke.tprint("Render Folder already exists!")
					
				fileName = readFile.split('/')[ - 1]
				fileNameTable = fileName.split('.')
				newFileName = ""
				
				for i in range(0, len(fileNameTable) -1):
					newFileName += fileNameTable[i] + "."
					
				newPath += newFileName
				
				if dialog.window.value("File Format:") == "exr":
					newPath += "exr"
				if dialog.window.value("File Format:") == "jpeg":
					newPath += "jpg"
				if dialog.window.value("File Format:") == "png":
					newPath += "png"
				if dialog.window.value("File Format:") == "tiff":
					newPath += "tif"
				
				if dialog.window.value("Reformat?") == 1:
					reformat = nuke.createNode("Reformat")
					nuke.extractSelected()
					reformat.knob('xpos').setValue(nodeXPos)
					reformat.knob('ypos').setValue(nodeYPos + 150)
					reformat.knob('filter').setValue(dialog.window.value("Reformat Filter:"))
					
					print newWidth
					print newHeight
					
					reformat.knob('type').setValue("to box")
					reformat.knob('box_fixed').setValue(1)
					reformat.knob('box_width').setValue(int(newWidth))
					reformat.knob('box_height').setValue(int(newHeight))
					
					write = nuke.createNode("Write")
					nuke.extractSelected()
					write.knob('xpos').setValue(nodeXPos)
					write.knob('ypos').setValue(nodeYPos + 300)
					
					reformat.setInput(0, n)
					write.setInput(0, reformat)
				else:
					write = nuke.createNode("Write")
					nuke.extractSelected()
					write.knob('xpos').setValue(nodeXPos)
					write.knob('ypos').setValue(nodeYPos + 150)
					
					write.setInput(0, n)
					
				write.knob('file').setValue(newPath)
				write.knob('file_type').setValue(dialog.window.value("File Format:"))
				
				if dialog.window.value("File Format:") == "exr":
					if exr.window.value("Data Type:") == "16_Bit_Half":
						write.knob('datatype').setValue("16 bit half")
					if exr.window.value("Data Type:") == "32_Bit_Float":
						write.knob('datatype').setValue("32 bit float")
					
					if exr.window.value("Compression:") == "Zip_1_Scanline":
						write.knob('compression').setValue("Zip (1 scanline)")
					if exr.window.value("Compression:") == "Zip_16_Scanlines":
						write.knob('compression').setValue("Zip (16 scanlines)")
					if exr.window.value("Compression:") == "PIZ_Wavelet_32_Scanlines":
						write.knob('compression').setValue("PIZ Wavelet (32 scanlines)")
					if exr.window.value("Compression:") == "RLE":
						write.knob('compression').setValue("RLE")
					if exr.window.value("Compression:") == "B44":
						write.knob('compression').setValue("B44")
					if exr.window.value("Compression:") == "None":
						write.knob('compression').setValue("none")
					
				if dialog.window.value("File Format:") == "jpeg":
					write.knob('_jpeg_quality').setValue(float(jpeg.window.value("Quality:")) / 100)
					
				if dialog.window.value("File Format:") == "png":
					if png.window.value("Data Type:") == "8_Bit":
						write.knob('datatype').setValue("8 bit")
					if png.window.value("Data_Type:") == "16_Bit":
						write.knob('datatype').setValue("16 bit")
					
				if dialog.window.value("File Format:") == "tiff":
					if tiff.window.value("Data Type:") == "8_Bit":
						write.knob('datatype').setValue("8 bit")
					if tiff.window.value("Data Type:") == "16_Bit":
						write.knob('datatype').setValue("16 bit")
					if tiff.window.value("Data Type:") == "32_Bit_Float":
						write.knob('datatype').setValue("32 bit float")
						
					if tiff.window.value("Compression:") == "Deflate":
						write.knob('compression').setValue("Deflate")
					if tiff.window.value("Compression:") == "LZW":
						write.knob('compression').setValue("LZW")
					if tiff.window.value("Compression:") == "PackBits":
						write.knob('compression').setValue("PackBits")
					if tiff.window.value("Compression:") == "None":
						write.knob('compression').setValue("none")
						
				n.knob('proxy').setValue(newPath)