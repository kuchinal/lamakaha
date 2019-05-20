# To test all the callbacks, add this to your ~/.nuke/init.py:
#  import callbacksTrace
# This will make them all print something to stdout so you can see
# when they are called.

import nuke

def _cb(name):
  nuke.tprint(name + " " + nuke.thisNode().name())

def _cbk(name):
  nuke.tprint(name + " " + nuke.thisNode().name() + "." + nuke.thisKnob().name())

nuke.addOnUserCreate(_cb, ("onUserCreate"))

nuke.addOnCreate(_cb, ("onCreate"))

nuke.addOnScriptLoad(_cb, ("onScriptLoad"))

nuke.addOnScriptSave(_cb, ("onScriptSave"))

nuke.addOnScriptClose(_cb, ("onScriptClose"))

nuke.addOnDestroy(_cb, ("onDestroy"))

nuke.addKnobChanged(_cbk, ("knobChanged"))

nuke.addUpdateUI(_cb, ("updateUI"))

nuke.addAutolabel(_cb, ("autolabel"))

nuke.addBeforeRender(_cb, ("beforeRender"))

nuke.addBeforeFrameRender(_cb, ("beforeFrameRender"))

nuke.addAfterFrameRender(_cb, ("afterFrameRender"))

nuke.addAfterRender(_cb, ("afterRender"))

nuke.addFilenameFilter(lambda s: nuke.tprint("filenameFilter('"+s+"')"))
