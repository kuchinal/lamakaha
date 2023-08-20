def playSound():
     import nuke
     import os
     import nukescripts
     macSound = 'PATH/TO/SOUND/FILE'
     winSound =  os.path.dirname(nuke.env['ExecutablePath']) + '/'+ 'plugins/user/user/Beep.WAV'
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

 # TopDir = os.path.dirname(nuke.env['ExecutablePath']) + '/';
 # if nuke.env['MACOS']:
   # TopDir = os.path.abspath(TopDir + '../../../') + '/'
  #nukescripts.start(TopDir + 'plugins/user/user/Beep.WAV')