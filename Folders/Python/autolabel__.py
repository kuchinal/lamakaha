# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import os
import nuke

def __concat_result_string(name, label):
  if label is None or label == "":
    return name
  return str(name + "\n" + label).strip()

def autolabel():
  """This function is run automatically by Nuke during idle, and the return
  text is drawn on the box of the node. It can also have side effects by
  setting knobs. Currently two knobs are provided that are useful:
  
  indicators = integer bit flags to turn icons on/off. The icons
  named indicator1, indicator2, indicator4, indicator8, etc are
  drawn if the corresponding bit is on. By default these are loaded
  from the path as indicator1.xpm, etc, but you can use the load_icon
  command to load other files.
  
  icon = name of a whole extra image you can draw, but it replaces
  any previous one."""
  
  # do the icons:
  ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)")

  if int(nuke.numvalue("maskChannelInput", 0)) :
    ind += 4
  if int(nuke.numvalue("this.mix", 1)) < 1:
    ind += 16
  nuke.knob("this.indicators", str(ind))

  this = nuke.toNode("this")

  # do stuff that works even if autolabel is turned off:
  name = nuke.value("name")
  _class = this.Class()

  label = nuke.value("label")
  if not label:
    label = ""
  else:
    try:
      label = nuke.tcl("subst", label)
    except:
      pass
      
  if _class == "Dot" or _class == "BackdropNode" or _class == "StickyNote":
    return label
  elif _class.startswith("Read") or _class.startswith("Write") or _class.startswith( "Precomp" ):
    reading = int(nuke.numvalue("this.reading", 0 ))

    if reading and _class.startswith( "Precomp" ):
      filename = nuke.filename( node = this.output().input(0), replace = nuke.REPLACE )
    else:
      filename = nuke.filename(replace = nuke.REPLACE)
    if filename is not None:
      name = __concat_result_string(name, os.path.basename(filename))
    
    if reading:
      checkHashOnRead = False
      if _class.startswith( "Precomp" ):
        if this.output() != None and this.output().input(0) != None:
          checkHashOnReadKnob = this.output().input(0).knob( "checkHashOnRead" )
          if checkHashOnReadKnob:
            checkHashOnRead = checkHashOnReadKnob.value()
      else:
        checkHashOnRead = this.knob("checkHashOnRead").value()
        
      if checkHashOnRead == True and ( this.proxy() != True ):
        name = name + "\n(Read)"
      else:
        name = name + "\n(Read - unchecked)"

  if nuke.numvalue("preferences.autolabel") == 0 or _class.find("OFX", 0) != -1:
    return __concat_result_string(name, label)

  # build the autolabel:
  operation = nuke.value('this.operation', '')
  if operation != '' and _class != 'ChannelMerge' and _class != 'Precomp':
    name = name + ' (' + operation + ')'

  layer = nuke.value("this.output", nuke.value("this.channels", "-"))
  mask = nuke.value("this.maskChannelInput", "none")
  unpremult = nuke.value("this.unpremult", "none")
  
  if _class.startswith("Read"):
    if int(nuke.numvalue("this.raw", 0)):
      layer = "RAW"
    elif int(nuke.numvalue("this.colorspace", 0)):
      layer = nuke.value("colorspace")
  elif _class.startswith("Write"):
    if int(nuke.numvalue("this.raw", 0)):
      layer = "RAW"
    elif int(nuke.numvalue("this.colorspace", 0)):
      layer = nuke.value("colorspace")
    order = nuke.numvalue("this.render_order", 1)
    mask = str(order)
    if int(order) == 1:
      mask = "none"
  elif _class == "Reformat":
    if nuke.expression("!type"):
      format = nuke.value("format")
      rootformat = nuke.value("root.format")
      if format is not None and format != rootformat:
        format_list = format.split()
        layer = " ".join(format_list[7:])
  elif _class == "ChannelMerge":
    if operation == "union":
      operation = "U"
    elif operation == "intersect":
      operation = "I"
    elif operation == "stencil":
      operation = "S"
    elif operation == "absminus":
      operation = "abs-"
    elif operation == "plus":
      operation = "+"
    elif operation == "minus":
      operation = "-"
    elif operation == "multiply":
      operation = "*"
    layer = nuke.value("A") + " " + operation + " " + nuke.value("B") + " =\n" + nuke.value("output")
  elif _class == "Premult" or _class == "Unpremult":
    unpremult = nuke.value("alpha")
    if unpremult == "alpha":
      unpremult = "none"
  elif _class == "Copy":
    layer = ""
    if nuke.value("to0") != "none":
      layer += nuke.value("from0") + " -> " + nuke.value("to0")
    if nuke.value("to1") != "none":
      layer += "\n" + nuke.value("from1") + " -> " + nuke.value("to1")
    if nuke.value("to2") != "none":
      layer += "\n" + nuke.value("from2") + " -> " + nuke.value("to2")
    if nuke.value("to3") != "none":
      layer += "\n" + nuke.value("from3") + " -> " + nuke.value("to3")
    if nuke.value("channels") != "none":
      layer += ("\n" + nuke.value("channels") + "->" + nuke.value("channels"))
  elif _class == "FrameHold":
    value_inc = nuke.value("increment")
    if int(value_inc):
      layer = "frame "+nuke.value("knob.first_frame")+"+n*"+value_inc
    else:
      layer = "frame "+nuke.value("knob.first_frame")
  elif _class == "Precomp":
    layer = '-'

  if mask != "none":
    if int(nuke.numvalue("invert_mask", 0)):
      layer += (" / ~" + mask)
    else:
      layer += (" / " + mask)

  if unpremult != "none" and unpremult != mask:
    layer += ( " / " + unpremult)

  if layer != "rgba" and layer != "rgb" and layer != "-":
    result = __concat_result_string(name, "(" + layer + ")" + "\n" + label)
  else:
    result = __concat_result_string(name, label)
  
  return result

