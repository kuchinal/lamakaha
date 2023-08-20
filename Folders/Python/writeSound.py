

# Developed by Christian Castaneda
# chris@castanedafx.com
# This should create a custom write node that plays a sound when finished rendering
import nuke

nukeOriginalWriteSoundNode = nuke.createNode

def attachWriteSoundNode():
   nuke.createNode = customWriteSoundNode

def customWriteSoundNode(node, knobs = "", inpanel = True):
   if node == "Write":
     writeNode = nukeOriginalWriteSoundNode( node, knobs, inpanel )
     ## attach our custom tab
     createWriteSoundTab( writeNode )
     return writeNode
   else:
     return nukeOriginalWriteSoundNode( node, knobs, inpanel )

def createWriteSoundTab(node):
 #### create knobs
 tabKnob = nuke.Tab_Knob('WriteSound')
 channelKnob = nuke.Link_Knob('channels_name', 'channels')
 fileKnob = nuke.Link_Knob('file_name', 'file')
 proxyKnob = nuke.Link_Knob('proxy_name', 'proxy')
 divideKnob = nuke.Text_Knob('')
 colorKnob = nuke.Link_Knob('colorspace_name', 'colorspace')
 preMultKnob = nuke.Link_Knob('premultiplied_name', 'premultiplied')
 rawDataKnob = nuke.Link_Knob('raw data name', 'raw data')
 viewsKnob = nuke.Link_Knob('views_name', 'views')
 typeKnob = nuke.Link_Knob('file type name', 'file type')
 orderKnob = nuke.Link_Knob('render_order_name', 'render order')
 buttonKnob = nuke.PyScript_Knob('Render With Sound')
 
 #### make links to the Original Write
 channelKnob.setLink('channels')
 fileKnob.setLink('file')
 proxyKnob.setLink('proxy')
 colorKnob.setLink('colorspace')
 preMultKnob.setLink('premultiplied')
 rawDataKnob.setLink('raw')
 viewsKnob.setLink('views')
 typeKnob.setLink('file_type')
 orderKnob.setLink('render_order')

 script = """
############ This section by Fredrik Brannbacka #############
##
## Make sure you set the sounds file path
macSound = 'PATH/TO/SOUND/FILE'
winSound = 'C:/Program Files (x86)/Nuke5.1v5/plugins/user/BIP.wav'
def playSound():
  if nuke.env["MACOS"]:
      sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python')
      sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python/PyObjC')
      from AppKit import NSSound
      sound = NSSound.alloc()
      sound.initWithContentsOfFile_byReference_(macSound, True)
      sound.play()
  elif nuke.env["WIN32"]:
      import winsound
      winsound.PlaySound(winSound, winsound.SND_FILENAME|winsound.SND_ASYNC)

node = nuke.selectedNode()
if node.Class()=='Write':
  start,end = nuke.getFramesAndViews('Render Range','%i,%i' % (nuke.root()['first_frame'].value(),nuke.root()['last_frame'].value()))[0].split(',',2)
  if nuke.execute(node.name(),int(start),int(end)):
   playSound()
"""

 buttonKnob.setValue(script)
 
 #### add knobs to node
 for k in [tabKnob, channelKnob, fileKnob, proxyKnob, divideKnob, colorKnob, preMultKnob, rawDataKnob, viewsKnob, typeKnob, orderKnob, buttonKnob]:
     node.addKnob(k) 