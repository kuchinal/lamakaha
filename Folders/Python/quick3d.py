# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# 
# Example that shows how to hook up nodes to create a simple 3d setup
#

import nuke

def quick3d():
  ## create the three nodes

  axis = nuke.Axis()
  card = nuke.nodes.Card()
  tran = nuke.TransformGeo()

  cam = nuke.nodes.Camera()

  scene = nuke.nodes.Scene()
  render = nuke.nodes.ScanlineRender()
  
  ## hook them up
  render.setInput(1, scene )
  render.setInput(2, cam )
  scene.setInput(0,cam)
  scene.setInput(1,tran)

  
