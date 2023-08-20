# Copyright (c) 2010 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Adapted for basic JefeCheck support by Frank Rueter

import os.path
import re
import nuke
import subprocess
from nukescripts import flipbooking

class JefeCheckFlipbook(flipbooking.FlipbookApplication):
  # Discover the location of JefeCheck on construction
  def __init__(self):
    self._jcPath = ""
    try:
      self._jcPath = os.environ["JC_PATH"]
    except:
      raise ValueError, '"JC_PATH" not set. Need environment valrialbe "JC_PATH" to be set and pointing go JefeCheck'
    self._jcPath = os.path.normpath(self._jcPath)

  ##############################################################
  # Interface implementation 
  ##############################################################
  def name(self):
    """
    Return the name of the flipbook.
    @return: String
    """    
    return "JefeCheck"

  def path(self):
    """
    Return the executable path required to run a flipbook.
    @return: String
    """    
    return self._jcPath

  def cacheDir(self):
    """
    Return the preferred directory for rendering.
    @return: String
    """
    return os.environ["NUKE_TEMP_DIR"]
    #try:
      #cachePath = os.environ["JC_CACHE__PATH"]
    #except:
      #cachePath = nuke.value('preferences.DiskCachePath')
      #cachePath = os.join(cachePath, 'jefeCheckCache')
      #if not os.path.isdir(cachePath):
        #os.makedirs(cachePath)
    #return cachePath

  def convertPadding(self, imagePath):
    # TURN %d NOTATION INTO HASHES
    pattern = re.compile("%([0-9]*)d")
    match = re.search(pattern, imagePath)
    if match:
      return re.sub(pattern, '#'*int(match.group(1)), imagePath)
    else:
      return imagePath

  def run(self, imagePath, frameRanges, views, options):
    print "TEST"
    args = []
    args.append( self.path() )
    args.append( self.convertPadding(imagePath) )
    args += ['-f', str(frameRanges.minFrame()), '-t', str(frameRanges.maxFrame())]

    print frameRanges
    print args

    subprocess.Popen( args )


  def capabilities(self):
    return { 
      'proxyScale': False,
      'crop': False,
      'canPreLaunch': False, 
      'supportsArbitraryChannels': False, 
      'maximumViews' : 2,
      'fileTypes' : ['dpx', 'tif', 'iff', 'exr', 'jpg', 'cin', 'png', 'sgi', 'bmp', 'tga', 'rgb']
    }
  

# register the flipbook app.
jc = JefeCheckFlipbook()
flipbooking.register(jc)

