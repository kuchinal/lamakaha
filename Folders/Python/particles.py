# -*- coding: utf-8 -*-
from __future__ import with_statement
import nuke
import _nukemath
import random
import os

# -----------------------------------------------------------------------------

#def inc(v):
#    v[0] += 1

# -----------------------------------------------------------------------------

def CreateGroup():
    nuke.tcl('particlesGroup.tcl')

# -----------------------------------------------------------------------------

def ParticlesCallback():
    n = nuke.thisNode()

    if (n['__ISPARTICLESYSTEM'] == None):
      return

    k = nuke.thisKnob()

    if (k.name() == 'colorInterpolation'):
        if (k.value() == 'none'):
            n['deathColor'].setEnabled(False)
            n['deathColorVariance'].setEnabled(False)
        else:
            n['deathColor'].setEnabled(True)
            n['deathColorVariance'].setEnabled(True)
        if (k.value() == 'custom'):
            n['customColorCurve'].setEnabled(True)
            n['customColorCurve'].setVisible(True)
        else:
            n['customColorCurve'].setEnabled(False)
            n['customColorCurve'].setVisible(False)
    elif (k.name() == 'transparencyInterpolation'):
        if (k.value() == 'none'):
            n['deathTransparency'].setEnabled(False)
            n['deathTransparencyVariance'].setEnabled(False)
        else:
            n['deathTransparency'].setEnabled(True)
            n['deathTransparencyVariance'].setEnabled(True)
        if (k.value() == 'custom'):
            n['customTransparencyCurve'].setEnabled(True)
            n['customTransparencyCurve'].setVisible(True)
        else:
            n['customTransparencyCurve'].setEnabled(False)
            n['customTransparencyCurve'].setVisible(False)
    elif (k.name() == 'sizeInterpolation'):
        if (k.value() == 'none'):
            n['deathSize'].setEnabled(False)
            n['deathSizeVariance'].setEnabled(False)
        else:
            n['deathSize'].setEnabled(True)
            n['deathSizeVariance'].setEnabled(True)
        if (k.value() == 'custom'):
            n['customSizeCurve'].setEnabled(True)
            n['customSizeCurve'].setVisible(True)
        else:
            n['customSizeCurve'].setEnabled(False)
            n['customSizeCurve'].setVisible(False)
    elif (k.name() == 'emitterType'):
        if (k.value() == 'Points from OBJ'):
            n['objFileName'].setVisible(True)
        else:
            n['objFileName'].setVisible(False)
    elif (k.name() == 'objFileName'):
        with nuke.toNode(nuke.thisNode().fullName() + ".Group"):
            nuke.toNode('objVisualization')['file'].setValue(k.value())
    elif (k.name() == 'applyMaterial'):
	with nuke.toNode(nuke.thisNode().fullName() + ".Group"):
	  ApplyMaterials(k.value())
    elif (k.name() == 'firstImg'):
      with nuke.toNode(nuke.thisNode().fullName() + ".Group"):
        ImageSwitch(not k.value())
    elif (k.name() == 'cacheTextures'):
      with nuke.toNode(nuke.thisNode().fullName() + ".Group"):
        CacheTextures(k.value())
    elif (k.name() == 'showPanel'):
        if (n['sizeInterpolation'].value() != 'custom'):
            n['customSizeCurve'].setEnabled(False)
            n['customSizeCurve'].setVisible(False)
        if (n['colorInterpolation'].value() != 'custom'):
            n['customColorCurve'].setEnabled(False)
            n['customColorCurve'].setVisible(False)
        if (n['transparencyInterpolation'].value() != 'custom'):
            n['customTransparencyCurve'].setEnabled(False)
            n['customTransparencyCurve'].setVisible(False)
        if (n['emitterType'].value() != 'Points from OBJ'):
            n['objFileName'].setVisible(False)

# -----------------------------------------------------------------------------
            
def ChooseImageSource(img1Connected, img2Connected, img3Connected, random):
    if not (img1Connected or img2Connected or img3Connected) : return 3
    connectedInputs = []
    if (img1Connected): connectedInputs.append(0)
    if (img2Connected): connectedInputs.append(1)
    if (img3Connected): connectedInputs.append(2)
    return connectedInputs[int(random * len(connectedInputs))]

# -----------------------------------------------------------------------------

def GetRandomSeed(seedOffset = 0, seedScale = 1):
    return '(parent.parent.randomSeed + ' + str(seedOffset) + ') * ' + str(seedScale)

# -----------------------------------------------------------------------------

def GetRandomSeedTriple(seedOffset = 0, seedScale = 1):
    randomSeed = GetRandomSeed(seedOffset, seedScale)
    return randomSeed + ', ' + randomSeed + ', ' + randomSeed

# -----------------------------------------------------------------------------

def GetOBJVertices (objFileName):
    vertices = []
    
    file = None
    try:
        file = open(objFileName, 'r')
        for line in file:
            words = line.split()
            if words[0] == 'v':
                x, y, z = float(words[1]), float(words[2]), float(words[3])
                vertices.append(_nukemath.Vector3(x,y,z))
    except IOError:
        nuke.message('Error while processing the file ' + objFileName)
    finally:
        if (file != None): file.close()

    return vertices

# -----------------------------------------------------------------------------

def ApplyMaterials(apply):
    curNode = 0
    if (apply):
        ApplyMaterials(False)
        n = nuke.toNode('color' + str(curNode))
        while (n != None):
            applyMaterial = nuke.nodes.ApplyMaterial(label='auto',name='applyMaterial'+str(curNode))
            applyMaterial.setInput(0, nuke.toNode('geo'))
            n2 = nuke.toNode('diskCache' + str(curNode))
            if (n2 != None):
                applyMaterial.setInput(1, n2)
            else:
                applyMaterial.setInput(1, n)
            applyMaterial['disable'].setExpression('!particleRoot' + str(curNode) +'.alive')
            nuke.toNode('translate' + str(curNode)).setInput(0, applyMaterial)
            nuke.autoplace(applyMaterial)

            curNode += 1
            n = nuke.toNode('color' + str(curNode))
    else:
        n = nuke.toNode('applyMaterial' + str(curNode))
        while (n != None):
            nuke.delete(n)
            curNode += 1
            n = nuke.toNode('applyMaterial' + str(curNode))

# -----------------------------------------------------------------------------

def CacheTextures(cache):
    curNode = 0
    if (cache):
        CacheTextures(False)
        n = nuke.toNode('color' + str(curNode))
        while (n != None):
            cache = nuke.nodes.DiskCache(label='auto',name='diskCache'+str(curNode))
            cache.setInput(0, n)
            cache['disable'].setExpression('!particleRoot' + str(curNode) +'.alive')
            applyMaterial = nuke.toNode('applyMaterial' + str(curNode))
            if (applyMaterial != None):
                applyMaterial.setInput(1, cache)
            nuke.autoplace(cache)

            curNode += 1
            n = nuke.toNode('color' + str(curNode))
    else:
        n = nuke.toNode('diskCache' + str(curNode))
        while (n != None):
            nuke.delete(n)
            curNode += 1
            n = nuke.toNode('diskCache' + str(curNode))

# -----------------------------------------------------------------------------

def ImageSwitch(enable):
    curNode = 0
    if (enable):
        ImageSwitch(False)
        n = nuke.toNode('particleRoot' + str(curNode))
        while (n != None):
	  imageSwitch = nuke.nodes.Switch(label='auto',name='imageSwitch'+str(curNode))
	  imageSwitch.setInput(0, nuke.toNode('img1'))
	  imageSwitch.setInput(1, nuke.toNode('img2'))
	  imageSwitch.setInput(2, nuke.toNode('img3'))
	  imageSwitch.setInput(3, nuke.toNode('defaultTextureReformat'))
	  imageSwitch['which'].setExpression('[python particles.ChooseImageSource(nuke.thisParent().input(nuke.thisNode().input(0).knob("number").value()).input(0).knob("connected").value(),nuke.thisParent().input(nuke.thisNode().input(1).knob("number").value()).input(0).knob("connected").value(),nuke.thisParent().input(nuke.thisNode().input(2).knob("number").value()).input(0).knob("connected").value(),' + str(random.random()) + ')]')
	  n.setInput(0,imageSwitch)

          nuke.autoplace(imageSwitch)

          curNode += 1
          n = nuke.toNode('particleRoot' + str(curNode))
    else:
        n = nuke.toNode('imageSwitch' + str(curNode))
        while (n != None):
            nuke.delete(n)
	    nuke.toNode('particleRoot' + str(curNode)).setInput(0, nuke.toNode('img1'))
            curNode += 1
            n = nuke.toNode('imageSwitch' + str(curNode))

# -----------------------------------------------------------------------------

def MotionEquation(startPosition, startVelocity, acceleration, time):
    return startPosition.__add__((startVelocity.__mul__(time)).__add__(acceleration.__mul__(0.5 * time * time)))

# -----------------------------------------------------------------------------

def Update(transformNode, gizmoNode, frame, bakeSimulation = False, onlyUpdateIfAlive = True):
    #undo = nuke.Undo()
    #undo.name('Update Particles')
    #undo.begin()
    #undo.disable()

    #print (str(transformNode.name()) + ' ' + str(gizmoNode.name()) + ' ' + str(frame) + ' ' + str(Simulation))

    fps = nuke.root().fps()

    # update only if the current particle is alive
    if ((not onlyUpdateIfAlive) or nuke.toNode(transformNode['particleRoot'].value())['alive'].valueAt(frame)):
        position = _nukemath.Vector3(transformNode['transformedStartPosition'].x(),transformNode['transformedStartPosition'].y(),transformNode['transformedStartPosition'].z())

        birth = nuke.toNode(transformNode['particleRoot'].value())['birth'].value()
        death = nuke.toNode(transformNode['particleRoot'].value())['death'].value()
        frameRange = range(int(birth),frame)

        acceleration = _nukemath.Vector3(0,0,0)
        velocity = _nukemath.Vector3(transformNode['startVelocity'].valueAt(birth,0),transformNode['startVelocity'].valueAt(birth,1),transformNode['startVelocity'].valueAt(birth,2)).__div__(fps).__div__(transformNode['mass'].valueAt(birth))
        turbulence = _nukemath.Vector3(0,0,0)

        # integrate from birth to current frame
        for f in frameRange:
            mass = transformNode['mass'].valueAt(f)
            gravity = _nukemath.Vector3(gizmoNode['gravity'].valueAt(f,0),gizmoNode['gravity'].valueAt(f,1),gizmoNode['gravity'].valueAt(f,2)).__div__(fps).__mul__(0.25 * mass) # mass multiplication trick to strengthen the effect of air resistance
            externalForce = _nukemath.Vector3(gizmoNode['externalForce'].valueAt(f,0),gizmoNode['externalForce'].valueAt(f,1),gizmoNode['externalForce'].valueAt(f,2)).__div__(fps)
            drag = velocity.__mul__(-gizmoNode['drag'].valueAt(f))

            turbulenceAmount = _nukemath.Vector3(gizmoNode['turbulenceAmount'].valueAt(f,0), gizmoNode['turbulenceAmount'].valueAt(f,1), gizmoNode['turbulenceAmount'].valueAt(f,2))

            # apply simple equation if parameters stay constant and no turbulence or collision have to be considered on the way
            if (gizmoNode['parametersConstant'].valueAt(f) and (abs(gizmoNode['drag'].valueAt(f)) < 0.0000001) and (turbulenceAmount.lengthSquared() < 0.000000001) and (not gizmoNode['plane1Activate'].valueAt(f))):
                if (not bakeSimulation):
                    if (f == int(birth)):
                        p = MotionEquation(position, velocity, gravity.__add__((externalForce.__add__(drag)).__div__(mass)), frame - birth)
                        transformNode['translate'].setValue(p.x,0)
                        transformNode['translate'].setValue(p.y,1)
                        transformNode['translate'].setValue(p.z,2)
                        return 0
##                else:
##                        p = MotionEquation(position, velocity, gravity.__add__((externalForce.__add__(drag)).__div__(mass)), f - birth)
##                        transformNode['translate'].setValue(p.x,0)
##                        transformNode['translate'].setValue(p.y,1)
##                        transformNode['translate'].setValue(p.z,2)
##                        transformNode['translate'].setKeyAt(f)
##                        continue

            if (turbulenceAmount.lengthSquared() > 0.000000001):
                randomSeed = gizmoNode['randomSeed'].valueAt(f) + 10 * transformNode['particleNumber'].value()
                turbulence = _nukemath.Vector3(\
                    turbulenceAmount.x * (nuke.expr('random(' + str(position.x * gizmoNode['turbulenceFrequency'].valueAt(f,0)) + ',' + str(randomSeed) + ',' + str(randomSeed) + ')') - 0.5),\
                    turbulenceAmount.y * (nuke.expr('random(' + str(randomSeed) + ',' + str(position.y * gizmoNode['turbulenceFrequency'].valueAt(f,1)) + ',' + str(randomSeed) + ')') - 0.5),\
                    turbulenceAmount.z * (nuke.expr('random(' + str(randomSeed) + ',' + str(randomSeed) + ',' + str(position.z * gizmoNode['turbulenceFrequency'].valueAt(f,2)) + ')') - 0.5)).__div__(fps)

            acceleration = gravity.__add__(((externalForce.__add__(turbulence)).__add__(drag)).__div__(mass))
            velocity = velocity.__add__(acceleration)

            oldPosition = _nukemath.Vector3(position.x, position.y, position.z)
            position = position.__add__(velocity)

            if (gizmoNode['plane1Activate'].valueAt(f)):
                n = _nukemath.Vector3(gizmoNode['plane1NormalizedNormal'].valueAt(f,0), gizmoNode['plane1NormalizedNormal'].valueAt(f,1), gizmoNode['plane1NormalizedNormal'].valueAt(f,2))
                d = gizmoNode['plane1DistanceFromOrigin'].valueAt(f) - gizmoNode['collisionRadius'].valueAt(f)
                if ((_nukemath.Vector3.distanceFromPlane(position, n.x, n.y, n.z, d)) < 0):
                    u = (n.x * oldPosition.x + n.y * oldPosition.y + n.z * oldPosition.z + d) / (n.x * (oldPosition.x - position.x) + n.y * (oldPosition.y - position.y) + n.z * (oldPosition.z - position.z))
                    position = oldPosition.__add__(velocity.__mul__(u))
                    velocity = (velocity.__sub__(n.__mul__(2 * n.dot(velocity)))).__mul__(gizmoNode['bounceAmount'].valueAt(f))

            if (bakeSimulation):
                transformNode['translate'].setValue(position.x,0,f)
                transformNode['translate'].setValue(position.y,1,f)
                transformNode['translate'].setValue(position.z,2,f)
                transformNode['translate'].setKeyAt(f)

        if (not bakeSimulation):
            transformNode['translate'].setValue(position.x,0)
            transformNode['translate'].setValue(position.y,1)
            transformNode['translate'].setValue(position.z,2)
        #undo.cancel()
        #undo.end()
    
    return 0

# -----------------------------------------------------------------------------

def ResetTransformExpressions(node, clear):
    if (clear):
	node['transformedStartPosition'].clearAnimated()
	node['transformedStartPosition2'].clearAnimated()
	node['startVelocity'].clearAnimated()
	node['mass'].clearAnimated()
    else:
	node['transformedStartPosition'].setExpression(node['transformedStartPositionExpressionX'].value(),0)
	node['transformedStartPosition'].setExpression(node['transformedStartPositionExpressionY'].value(),1)
	node['transformedStartPosition'].setExpression(node['transformedStartPositionExpressionZ'].value(),2)
	node['transformedStartPosition2'].setExpression(node['transformedStartPosition2ExpressionX'].value(),0)
	node['transformedStartPosition2'].setExpression(node['transformedStartPosition2ExpressionY'].value(),1)
	node['transformedStartPosition2'].setExpression(node['transformedStartPosition2ExpressionZ'].value(),2)
	node['startVelocity'].setExpression(node['startVelocityExpressionX'].value(),0)
	node['startVelocity'].setExpression(node['startVelocityExpressionY'].value(),1)
	node['startVelocity'].setExpression(node['startVelocityExpressionZ'].value(),2)
	node['mass'].setExpression(node['massExpression'].value())

# -----------------------------------------------------------------------------

def BakeSimulation(bake):
    this = nuke.thisNode()
    this['unbakeSimulation'].setEnabled(bake)

    with nuke.toNode(nuke.thisNode().fullName() + ".Group"):

      curNode = 0
      n = nuke.toNode('translate' + str(curNode))
      while (n != None):
	  if (bake):
	      ResetTransformExpressions(n, False)
	      n['pivot'].clearAnimated(0)
	      n['translate'].setAnimated()
	      Update(n, this, int(nuke.toNode(n['particleRoot'].value())['birth'].value() + nuke.toNode(n['particleRoot'].value())['death'].value() + 1), True, False)
	      ResetTransformExpressions(n, True)
	  else:
	      ResetTransformExpressions(n, False)
	      n['translate'].clearAnimated()
	      n['pivot'].setExpression('0 * (!' + n['particleRoot'].value() + '.alive || [ python particles.Update(nuke.thisNode(), nuke.toNode("' + this.fullName() + '"), nuke.frame()) ])',0)
	  curNode += 1
	  n = nuke.toNode('translate' + str(curNode))

# -----------------------------------------------------------------------------

def Generate():
    #try:
        undo = nuke.Undo()
        undo.name('Generate Particles')
        undo.begin()

        nuke.thisNode()['unbakeSimulation'].setEnabled(False)

        this = nuke.thisNode()

        with nuke.toNode(this.fullName() + ".Group"):
            # delete old nodes
            for n in nuke.allNodes():
                if (n['label'].value() == 'auto'): nuke.delete(n)

	    nuke.toNode('outScene').setInput(2, None)

            # load OBJ
            objVertices = []
            if (this['emitterType'].value() == 'Points from OBJ'):
                objVertices = GetOBJVertices(this['objFileName'].value())
            objVertexCount = len(objVertices)
            vertexIndices = range(objVertexCount)

            # generate particles
            frameRange = range(int(nuke.root().firstFrame() - this['prerollTime'].value() * nuke.root().fps()), nuke.root().lastFrame() + 1)
            curParticle = 0
            scene = None
            curSceneCount = 0
            exactParticlesAtFrame = 0.9999
            for f in frameRange:
                exactParticlesAtFrame += this['particlesPerSecond'].valueAt(f) / nuke.root().fps()
                if (int(exactParticlesAtFrame) - curParticle) > 0:
                    for p in range(int(exactParticlesAtFrame) - curParticle):

                        random.seed(int((this['randomSeed'].value()+curParticle+1)*(curParticle+1)))

                        # image switch
                        if (not this['firstImg'].value()):
                            imageSwitch = nuke.nodes.Switch(label='auto',name='imageSwitch'+str(curParticle))
                            imageSwitch.setInput(0, nuke.toNode('img1'))
                            imageSwitch.setInput(1, nuke.toNode('img2'))
                            imageSwitch.setInput(2, nuke.toNode('img3'))
                            imageSwitch.setInput(3, nuke.toNode('defaultTextureReformat'))
                            imageSwitch['which'].setExpression('[python particles.ChooseImageSource(nuke.thisParent().input(nuke.thisNode().input(0).knob("number").value()).input(0).knob("connected").value(),nuke.thisParent().input(nuke.thisNode().input(1).knob("number").value()).input(0).knob("connected").value(),nuke.thisParent().input(nuke.thisNode().input(2).knob("number").value()).input(0).knob("connected").value(),' + str(random.random()) + ')]')

                        # particle root dot
                        dot = nuke.nodes.Dot(label='auto',name='particleRoot'+str(curParticle))
                        if (not this['firstImg'].value()):
                            dot.setInput(0, imageSwitch)
                        else:
                            dot.setInput(0, nuke.toNode('img1'))

                        # calculate life and interpolation curves
                        lifeKnob = nuke.Double_Knob('life','life')
                        dot.addKnob(lifeKnob)
                        lifeKnob.setExpression('(1 + 2*parent.parent.lifeVariance*' + str((random.random()-0.5)) + ')*root.fps*parent.parent.life')
                        lifeKnob.setVisible(True)

                        birthKnob = nuke.Double_Knob('birth','birth')
                        dot.addKnob(birthKnob)
                        birthKnob.setExpression(str(f))
                        birthKnob.setVisible(True)

                        deathKnob = nuke.Double_Knob('death','death')
                        dot.addKnob(deathKnob)
                        deathKnob.setExpression('birth + life')
                        deathKnob.setVisible(True)

                        aliveKnob = nuke.Int_Knob('alive','alive')
                        dot.addKnob(aliveKnob)
                        aliveKnob.setExpression('inrange(frame,particleRoot' + str(curParticle) + '.birth,particleRoot' + str(curParticle) + '.death)')
                        aliveKnob.setVisible(True)

                        linearInterpolationKnob = nuke.Double_Knob('linearInterpolation','linearInterpolation')
                        dot.addKnob(linearInterpolationKnob)
                        linearInterpolationKnob.setExpression('min(1,max(0,1 - (frame - birth) / (death - birth)))')
                        linearInterpolationKnob.setVisible(True)

                        cosInterpolationKnob = nuke.Double_Knob('cosInterpolation','cosInterpolation')
                        dot.addKnob(cosInterpolationKnob)
                        cosInterpolationKnob.setExpression('1 - 0.5 * (cos(linearInterpolation*pi) + 1)')
                        cosInterpolationKnob.setVisible(True)

                        colorInterpolationKnob = nuke.Double_Knob('colorInterpolationValue','colorInterpolationValue')
                        dot.addKnob(colorInterpolationKnob)
                        colorInterpolationKnob.setExpression('(parent.parent.colorInterpolation == 0) + (parent.parent.colorInterpolation == 1) * particleRoot' + str(curParticle) + '.linearInterpolation + (parent.parent.colorInterpolation == 2) * particleRoot' + str(curParticle) + '.cosInterpolation  + (parent.parent.colorInterpolation == 3) * (1 - parent.parent.customColorCurve(1 + (frame - birth) / (death - birth)))')
                        #colorInterpolationKnob.setVisible(True)

                        testKnob = nuke.PyScript_Knob('test','test')
                        dot.addKnob(testKnob)
                        testKnob.setValue('nuke.message(str(nuke.toNode(nuke.thisParent().fullName().rpartition(".")[0]).knob("customColorCurve").value()))')

                        transparencyInterpolationKnob = nuke.Double_Knob('transparencyInterpolationValue','transparencyInterpolationValue')
                        dot.addKnob(transparencyInterpolationKnob)
                        transparencyInterpolationKnob.setExpression('(parent.parent.transparencyInterpolation == 0) + (parent.parent.transparencyInterpolation == 1) * particleRoot' + str(curParticle) + '.linearInterpolation + (parent.parent.transparencyInterpolation == 2) * particleRoot' + str(curParticle) + '.cosInterpolation  + (parent.parent.transparencyInterpolation == 3) * (1 - parent.parent.customTransparencyCurve(1 + (frame - birth) / (death - birth)))')
                        transparencyInterpolationKnob.setVisible(True)
                     
                        transparencyKnob = nuke.Double_Knob('transparency','transparency')
                        dot.addKnob(transparencyKnob)
                        transparencyKnob.setExpression('((1+2*parent.parent.birthTransparencyVariance*(pow(' + str(random.random()) + ',1+parent.parent.sRGBgammaTransparency*1.2)-0.5)) * particleRoot' + str(curParticle) + '.transparencyInterpolationValue * (parent.parent.birthTransparency) + (1+2*parent.parent.deathTransparencyVariance*(pow(' + str(random.random()) + ',1+parent.parent.sRGBgammaTransparency*1.2)-0.5)) * (1 - particleRoot' + str(curParticle) + '.transparencyInterpolationValue) * (parent.parent.deathTransparency))')
                        transparencyKnob.setVisible(True)

                        sizeInterpolationKnob = nuke.Double_Knob('sizeInterpolationValue','sizeInterpolationValue')
                        dot.addKnob(sizeInterpolationKnob)
                        sizeInterpolationKnob.setExpression('(parent.parent.sizeInterpolation == 0) + (parent.parent.sizeInterpolation == 1) * particleRoot' + str(curParticle) + '.linearInterpolation + (parent.parent.sizeInterpolation == 2) * particleRoot' + str(curParticle) + '.cosInterpolation + (parent.parent.sizeInterpolation == 3) * (1 - parent.parent.customSizeCurve(1 + (frame - birth) / (death - birth)))')
                        sizeInterpolationKnob.setVisible(True)

                        # texture frame offset
                        timeShift = nuke.nodes.TimeOffset(label='auto',name='timeOffset'+str(curParticle))
                        timeShift.setInput(0, dot)
                        timeShift['time_offset'].setExpression('-' + str(random.random()) + ' * (parent.parent.maxFrameShift + 1)')
                        timeShift['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        # premultiplied color + alpha
                        multiply = nuke.nodes.Multiply(label='auto',name='color'+str(curParticle))
                        multiply.setInput(0, timeShift)
                        multiply['value'].setSingleValue(False)
                        multiply['channels'].setValue('rgba')

			nextRandom = random.random()
			nextRandom2 = random.random()
                        multiply['value'].setExpression('(particleRoot' + str(curParticle) +'.transparency * ((1+2*parent.parent.birthColorVariance.r*(pow(' + str(nextRandom) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * particleRoot' + str(curParticle) + '.colorInterpolationValue * (parent.parent.birthColor.r) + (1+2*parent.parent.deathColorVariance.r*(pow(' + str(nextRandom2) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * (1 - particleRoot' + str(curParticle) + '.colorInterpolationValue) * (parent.parent.deathColor.r)))',0)
                        multiply['value'].setExpression('(particleRoot' + str(curParticle) +'.transparency * ((1+2*parent.parent.birthColorVariance.g*(pow(parent.parent.uniformVariance*' + str(nextRandom) + '+(1-parent.parent.uniformVariance)*' + str(random.random()) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * particleRoot' + str(curParticle) + '.colorInterpolationValue * (parent.parent.birthColor.g) + (1+2*parent.parent.deathColorVariance.g*(pow(parent.parent.uniformVariance*' + str(nextRandom2) + '+(1-parent.parent.uniformVariance)*' + str(random.random()) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * (1 - particleRoot' + str(curParticle) + '.colorInterpolationValue) * (parent.parent.deathColor.g)))',1)
                        multiply['value'].setExpression('(particleRoot' + str(curParticle) +'.transparency * ((1+2*parent.parent.birthColorVariance.b*(pow(parent.parent.uniformVariance*' + str(nextRandom) + '+(1-parent.parent.uniformVariance)*' + str(random.random()) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * particleRoot' + str(curParticle) + '.colorInterpolationValue * (parent.parent.birthColor.b) + (1+2*parent.parent.deathColorVariance.b*(pow(parent.parent.uniformVariance*' + str(nextRandom2) + '+(1-parent.parent.uniformVariance)*' + str(random.random()) + ',1+parent.parent.sRGBgammaColor*1.2)-0.5)) * (1 - particleRoot' + str(curParticle) + '.colorInterpolationValue) * (parent.parent.deathColor.b)))',2)
                        
                        multiply['value'].setExpression('particleRoot' + str(curParticle) +'.transparency',3)
                        
                        multiply['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        cache = None
                        if (this['cacheTextures'].value()):
                            cache = nuke.nodes.DiskCache(label='auto',name='diskCache'+str(curParticle))
                            cache.setInput(0, multiply)
                            cache['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        if (this['applyMaterial'].value()):
                            applyMaterial = nuke.nodes.ApplyMaterial(label='auto',name='applyMaterial'+str(curParticle))
                            applyMaterial.setInput(0, nuke.toNode('geo'))
                            if (this['cacheTextures'].value()):
                                applyMaterial.setInput(1, cache)
                            else:
                                applyMaterial.setInput(1, multiply)
                            applyMaterial['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        # translate
                        translateNode = nuke.nodes.TransformGeo(label='auto',name='translate'+str(curParticle))
                        translateNode['selectable'].setValue(False)
                        if (this['applyMaterial'].value()):
                            translateNode.setInput(0, nuke.toNode('applyMaterial' + str(curParticle)))
                        else:
                            translateNode.setInput(0, nuke.toNode('geo'))
                        translateNode.setInput(2, nuke.toNode('lookat'))
                        translateNode['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        # start position
                        startPosition = _nukemath.Vector3()
                        #startPositionKnob = nuke.XYZ_Knob('startPosition','startPosition')
                        #translateNode.addKnob(startPositionKnob)
                        if (this['emitterType'].value() == 'Point'):
                            startPosition.x = 0
                            startPosition.y = 0
                            startPosition.z = 0
                        elif (this['emitterType'].value() == 'Sphere'):
                            v = _nukemath.Vector3(random.random()-0.5,random.random()-0.5,random.random()-0.5)
                            while (v.lengthSquared() > 0.25):
                                v = _nukemath.Vector3(random.random()-0.5,random.random()-0.5,random.random()-0.5)
                            startPosition.x = v.x
                            startPosition.y = v.y
                            startPosition.z = v.z
                        elif (this['emitterType'].value() == 'Box'):
                            startPosition.x = random.random()-0.5
                            startPosition.y = random.random()-0.5
                            startPosition.z = random.random()-0.5
                        else:
                            indexListPosition = int(len(vertexIndices) * random.random())
                            vertexIndex = vertexIndices[indexListPosition]
                            del vertexIndices[indexListPosition]
                            if (len(vertexIndices) == 0):
                                vertexIndices = range(objVertexCount)
                            startPosition.x = objVertices[vertexIndex].x
                            startPosition.y = objVertices[vertexIndex].y
                            startPosition.z = objVertices[vertexIndex].z
                        #startPositionKnob.setVisible(True)

                        # transformed start position
                        transformedStartPositionKnob = nuke.XYZ_Knob('transformedStartPosition','transformedStartPosition')
                        translateNode.addKnob(transformedStartPositionKnob)
                        translate = 'parent.parent.position.x(particleRoot' + str(curParticle) + '.birth)'
			scale = 'parent.parent.scale.x(particleRoot' + str(curParticle) + '.birth)'
                        #translate = '[python nuke.toNode("' + this.fullName() + '").knob("position").valueAt(nuke.toNode("particleRoot' + str(curParticle) + '").knob("birth").value())\[0\]]'
                        #scale = '[python nuke.toNode("' + this.fullName() + '").knob("scale").valueAt(nuke.toNode("particleRoot' + str(curParticle) + '").knob("birth").value())\[0\]]'
                        expressionXKnob = nuke.String_Knob('transformedStartPositionExpressionX','transformedStartPositionExpressionX')
                        translateNode.addKnob(expressionXKnob)
                        expressionXKnob.setVisible(True)
                        expressionXKnob.setValue('(' + str(startPosition.x) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob.setExpression(expressionXKnob.value(),0)
                        
                        translate = 'parent.parent.position.y(particleRoot' + str(curParticle) + '.birth)'
			scale = 'parent.parent.scale.y(particleRoot' + str(curParticle) + '.birth)'
                        expressionYKnob = nuke.String_Knob('transformedStartPositionExpressionY','transformedStartPositionExpressionY')
                        translateNode.addKnob(expressionYKnob)
                        expressionYKnob.setVisible(True)
                        expressionYKnob.setValue('(' + str(startPosition.y) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob.setExpression(expressionYKnob.value(),1)
                        
                        translate = 'parent.parent.position.z(particleRoot' + str(curParticle) + '.birth)'
			scale = 'parent.parent.scale.z(particleRoot' + str(curParticle) + '.birth)'
                        expressionZKnob = nuke.String_Knob('transformedStartPositionExpressionZ','transformedStartPositionExpressionZ')
                        translateNode.addKnob(expressionZKnob)
                        expressionZKnob.setVisible(True)
                        expressionZKnob.setValue('(' + str(startPosition.z) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob.setExpression(expressionZKnob.value(),2)

                        # transformed start position one frame earlier
                        transformedStartPositionKnob2 = nuke.XYZ_Knob('transformedStartPosition2','transformedStartPosition2')
                        translateNode.addKnob(transformedStartPositionKnob2)
                        translate = 'parent.parent.position.x(particleRoot' + str(curParticle) + '.birth - 1)'
			scale = 'parent.parent.scale.x(particleRoot' + str(curParticle) + '.birth - 1)'
                        expressionXKnob = nuke.String_Knob('transformedStartPosition2ExpressionX','transformedStartPosition2ExpressionX')
                        translateNode.addKnob(expressionXKnob)
                        expressionXKnob.setVisible(True)
                        expressionXKnob.setValue('(' + str(startPosition.x) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob2.setExpression(expressionXKnob.value(),0)

                        translate = 'parent.parent.position.y(particleRoot' + str(curParticle) + '.birth - 1)'
			scale = 'parent.parent.scale.y(particleRoot' + str(curParticle) + '.birth - 1)'
                        expressionYKnob = nuke.String_Knob('transformedStartPosition2ExpressionY','transformedStartPosition2ExpressionY')
                        translateNode.addKnob(expressionYKnob)
                        expressionYKnob.setVisible(True)
                        expressionYKnob.setValue('(' + str(startPosition.y) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob2.setExpression(expressionYKnob.value(),1)

                        translate = 'parent.parent.position.z(particleRoot' + str(curParticle) + '.birth - 1)'
			scale = 'parent.parent.scale.z(particleRoot' + str(curParticle) + '.birth - 1)'
                        expressionZKnob = nuke.String_Knob('transformedStartPosition2ExpressionZ','transformedStartPosition2ExpressionZ')
                        translateNode.addKnob(expressionZKnob)
                        expressionZKnob.setVisible(True)
                        expressionZKnob.setValue('(' + str(startPosition.z) + ' * ' + scale + ' + ' + translate + ')')
                        transformedStartPositionKnob2.setExpression(expressionXKnob.value(),2)

			transformedStartPositionKnob.setVisible(True)
			transformedStartPositionKnob2.setVisible(True)

                        # start velocity force
                        startVelocityKnob = nuke.XYZ_Knob('startVelocity','startVelocity')
                        translateNode.addKnob(startVelocityKnob)

                        expressionXKnob = nuke.String_Knob('startVelocityExpressionX','startVelocityExpressionX')
                        translateNode.addKnob(expressionXKnob)
                        expressionXKnob.setVisible(True)
                        expressionXKnob.setValue('(1+2*parent.parent.velocityVariance.x*' + str((random.random() - 0.5)) + ') * parent.parent.startVelocity.x + 2 * ' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraVelocity.x + parent.parent.inherentEmitterVelocity * (transformedStartPosition.x - transformedStartPosition2.x)')
                        startVelocityKnob.setExpression(expressionXKnob.value(),0)

                        expressionYKnob = nuke.String_Knob('startVelocityExpressionY','startVelocityExpressionY')
                        translateNode.addKnob(expressionYKnob)
                        expressionYKnob.setVisible(True)
                        expressionYKnob.setValue('(1+2*parent.parent.velocityVariance.y*' + str((random.random() - 0.5)) + ') * parent.parent.startVelocity.y + 2 * ' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraVelocity.y + parent.parent.inherentEmitterVelocity * (transformedStartPosition.y - transformedStartPosition2.y)')
                        startVelocityKnob.setExpression(expressionYKnob.value(),1)
                        
                        expressionZKnob = nuke.String_Knob('startVelocityExpressionZ','startVelocityExpressionZ')
                        translateNode.addKnob(expressionZKnob)
                        expressionZKnob.setVisible(True)
                        expressionZKnob.setValue('(1+2*parent.parent.velocityVariance.z*' + str((random.random() - 0.5)) + ') * parent.parent.startVelocity.z + 2 * ' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraVelocity.z + parent.parent.inherentEmitterVelocity * (transformedStartPosition.z - transformedStartPosition2.z)')
                        startVelocityKnob.setExpression(expressionZKnob.value(),2)
                        
                        startVelocityKnob.setVisible(True)

                        # mass
                        massKnob = nuke.Double_Knob('mass','mass')
                        translateNode.addKnob(massKnob)
                        expressionKnob = nuke.String_Knob('massExpression','massExpression')
                        translateNode.addKnob(expressionKnob)
                        expressionKnob.setVisible(True)
                        expressionKnob.setValue('(1+2*parent.parent.massVariance*' + str((random.random() - 0.5)) + ') * parent.parent.mass')
                        massKnob.setExpression(expressionKnob.value())
                        massKnob.setVisible(True)

                        # store the particle number
                        particleNumberKnob = nuke.Int_Knob('particleNumber','particleNumber')
                        translateNode.addKnob(particleNumberKnob)
                        particleNumberKnob.setValue(curParticle)
                        particleNumberKnob.setVisible(True)

                        # store the particle root node
                        particleRootKnob = nuke.String_Knob('particleRoot','particleRoot')
                        translateNode.addKnob(particleRootKnob)
                        particleRootKnob.setValue('particleRoot' + str(curParticle))
                        particleRootKnob.setVisible(True)

                        # update function trigger
                        #updateTriggerKnob = nuke.Int_Knob('updateTrigger','updateTrigger')
                        #translateNode.addKnob(updateTriggerKnob)
                        #updateTriggerKnob.setExpression('!particleRoot' + str(curParticle) + '.alive || ')
                        #updateTriggerKnob.setVisible(True)
                        translateNode['pivot'].setExpression('0 * (!particleRoot' + str(curParticle) + '.alive || [ python particles.Update(nuke.thisNode(), nuke.toNode(nuke.thisParent().fullName().rpartition(".")\[0\]), nuke.frame()) ])',0)

                        # rotate + scale
                        rotateScale = nuke.nodes.TransformGeo(label='auto',name='rotateScale'+str(curParticle))
                        rotateScale['selectable'].setValue(False)
                        rotateScale.setInput(0, nuke.toNode('translate'+str(curParticle)))
                        rotateScale['disable'].setExpression('!particleRoot' + str(curParticle) +'.alive')

                        # calculate scale and rotation
			rotateScale['pivot'].setExpression('translate'+str(curParticle) + '.translate.x',0)
			rotateScale['pivot'].setExpression('translate'+str(curParticle) + '.translate.y',1)
			rotateScale['pivot'].setExpression('translate'+str(curParticle) + '.translate.z',2)

                        rotateScale['uniform_scale'].setExpression('(1+2*parent.parent.birthSizeVariance*' + str((random.random() - 0.5)) + ') * particleRoot' + str(curParticle) + '.sizeInterpolationValue * (parent.parent.birthSize) + (1+2*parent.parent.deathSizeVariance*' + str((random.random() - 0.5)) + ') * (1 - particleRoot' + str(curParticle) + '.sizeInterpolationValue) * (parent.parent.deathSize)')

                        startRotation = '(1+2*parent.parent.rotationVariance.x*' + str((random.random() - 0.5)) + ') * parent.parent.rotation.x + 2*' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraRotation.x'
                        rotation = startRotation + ' + frame / root.fps * ((1+2*parent.parent.rotationSpeedVariance.x*' + str((random.random() - 0.5)) + ') * parent.parent.rotationSpeed.x + 2*' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraRotationSpeed.x)'
                        rotateScale['rotate'].setExpression(rotation,0)
                        startRotation = '((1+2*parent.parent.rotationVariance.y*' + str((random.random() - 0.5)) + ') * parent.parent.rotation.y + 2*' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraRotation.y)'
                        rotation = startRotation + ' + frame / root.fps * ((1+2*parent.parent.rotationSpeedVariance.y*' + str((random.random() - 0.5)) + ') * parent.parent.rotationSpeed.y + 2*' + str((random.random() - 0.5)) + ' * parent.parent.maxExtraRotationSpeed.y)'
                        rotateScale['rotate'].setExpression(rotation,1)
                        startRotation = '((1+2*parent.parent.rotationVariance.z*' + str((random.random() - 0.5)) + ') * parent.parent.rotation.z + 2*' + str((random.random()) - 0.5) + ' * parent.parent.maxExtraRotation.z)'
                        rotation = startRotation + ' + frame / root.fps * ((1+2*parent.parent.rotationSpeedVariance.z*' + str((random.random() - 0.5)) + ') * parent.parent.rotationSpeed.z + 2*' + str((random.random() - 0.5)) +  ' * parent.parent.maxExtraRotationSpeed.z)'
                        rotateScale['rotate'].setExpression(rotation,2)

                        # switch to empty object if particle not alive
                        switch = nuke.nodes.Switch(label='auto',name='enableParticle'+str(curParticle))
                        switch.setInput(0, rotateScale)
                        #switch.setInput(1, nuke.toNode('emptyObject'))
                        switch['which'].setExpression('!particleRoot' + str(curParticle) + '.alive')

                        # add new scene if necessary
                        newSceneCount = int(curParticle / (998 + (curSceneCount == 1))) + 1
                        if (newSceneCount > curSceneCount):
                            newScene = nuke.nodes.Scene(label='auto')
                            if (scene != None):
                                newScene.setInput(0, scene)
                            scene = newScene
                            curSceneCount += 1
                            nuke.toNode('outScene').setInput(2, scene)

                        scene.setInput(curParticle % (998 + (curSceneCount == 1)) + (curSceneCount != 1), switch)
                        curParticle += 1

        nuke.root().setModified(True)
        undo.end()
    #except:
    #    nuke.message('Error while generating particles')
