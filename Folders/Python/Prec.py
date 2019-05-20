# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import os
import nuke
import autoBackdrop

def Prec():
   t = autoBackdrop.autoBackdrop()
   t['label'].setValue('PREC')
   t['bdwidth'].setValue(155)
   t['bdheight'].setValue(230 )
   t['tile_color'].setValue(2281701631)
