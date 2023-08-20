##################################################################################
#                                                                                #
#                             ANIMATION MAKER 1.1                                #
#                               David Emeny 2013                                 #
#                                                                                #
# This is a python/pyside extension to Nuke giving you prebuilt ease and wave    #
# expressions on any animatable knob. Just right click the knob and choose       #
# 'Animation maker...' from the pop up menu to display the interactive dialog.   #
# When you've tailored your animation, click CREATE and the expression required  #
# to produce that animation curve will be set on the knob in question.           #
# A custom tab will appear on the node too, so you can tweak your animation with #
# sliders. Click the EDIT button if you want to choose a different animation     #
# type. You can set Animation on any number of knobs within the same node.       #
#                                                                                #
##################################################################################


################# INSTALL INSTRUCTIONS #################
# Copy this file to your .nuke folder or plugins folder
# Add these lines to your menu.py:
# import AnimationMaker
# nuke.menu('Animation').addCommand( 'Animation Maker...', 'AnimationMaker.showWindow()','',icon='ParticleBounce.png')
########################################################


import nuke
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import random
import time
import math

def showWindow(knobName = None, knobIndex = None):
    
    #if no knobname is sent, this is called from the right click menu not a button
    if knobName == None:
        k = nuke.thisKnob()
    else:
        k = nuke.thisNode()[knobName]
    
    
    #see if there's more than one value (eg: x,y)
    if knobIndex == -1 or knobIndex == None:
        try:
            knobNames = []
            for i in range(0,len(k.value())):
                knobNames.append(k.name() + '.' + k.names(i))

            #ask user to choose one
            p = nuke.Panel("Which value?")
            p.addEnumerationPulldown("Knob value:", ' '.join(knobNames))
            
            p.addButton("Cancel")
            p.addButton("OK")
            pResult = p.show()
            
            if pResult == 1:
                #if OK was pressed, do stuff
                knobIndex = knobNames.index(p.value("Knob value:"))
                animationWindow(k.name(),knobIndex)

        except:
            #no sub knobs found, so open as normal
            animationWindow(k.name())
    else:
            animationWindow(k.name(),knobIndex)

    

class animationWindow(QtGui.QWidget):
    
    def __init__(self, knobName, knobIndex = -1, parent=None):
        
        super(animationWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        #make sure the widget is deleted when closed, so nuke doesn't crash on exit
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.theNode = nuke.thisNode()
        self.theKnob = self.theNode[knobName]
        self.origKnobName = knobName
        self.theKnobName = knobName
        
        #see if it's a multiple value knob
        try:
            self.knobAmount = len(self.theKnob.value())
            #print self.knobAmount
        except:
            self.knobAmount = 1
            #print self.knobAmount
            
        self.updateCreateButtonPressed = False
        
        #save the original value/keyframes/expression on that knob
        #so we can put it back again if they cancel
        self.originalValue = self.theKnob.toScript()
        
        self.knobIndex = knobIndex
        if self.knobIndex > -1:
            #there is more than one knob
            self.theKnobName += '_' + self.theKnob.names(self.knobIndex)
        
        
        #check if called from a knob that already has an associated tab
        theKnobs = self.theNode.knobs()
        if ("anim_tab_" + self.theKnobName) in theKnobs:
            self.editMode = True
        else:
            self.editMode = False
    
        if self.editMode:
            #check which kind of animation it is
            try:
                self.animType = self.theNode['a_animType_' + self.theKnobName].value()
            except:
                self.animType = "ease"
        else:
            self.animType = "ease"

        #set up window
        self.width = 600
        self.height = 600
        self.setGeometry(800, 200, self.width, self.height)
        self.setWindowTitle('Animation Maker - %s.%s' %(self.theNode.name(),self.theKnobName))
        
        #make close button
        if self.editMode:
            self.closeButton = QtGui.QPushButton('UPDATE', self)
        else:
            self.closeButton = QtGui.QPushButton('CREATE', self)
    
        self.closeButton.setGeometry(self.width-80, 225-50, 75, 46)
        self.closeButton.clicked.connect(self.closeButtonPressed)

        #make choice buttons
        buttonFont = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        
        self.easeButton = QtGui.QPushButton('Ease', self)
        self.easeButton.setGeometry(0, 0, 200, 112)
        self.easeButton.setFont(buttonFont)
        self.easeButton.clicked.connect(self.easeButtonPressed)

        self.waveButton = QtGui.QPushButton('Wave', self)
        self.waveButton.setGeometry(0, 112, 200, 112)
        self.waveButton.setFont(buttonFont)
        self.waveButton.clicked.connect(self.waveButtonPressed)
        

        #highlight relevant button
        if self.animType == "ease":
            self.easeButton.setStyleSheet('QWidget { background-color: #115511 }')
        elif self.animType == "wave" or self.animType == "waveEase":
            self.waveButton.setStyleSheet('QWidget { background-color: #115511 }')

        #make copyright text
        self.copyrightLabel = QtGui.QLabel(self)
        self.copyrightLabel.setText('<p style="font-family:arial;color:gray;font-size:10px;">David Emeny 2013</p>')
        self.copyrightLabel.move(self.width - 90, 0)
    
        self.easeBoxes = []
        self.waveBoxes = []

        self.setUpEaseBoxes()
    
        #set up different boxes if editing from wave or waveEase
        if self.editMode:
            if self.animType == "wave" or self.animType == "waveEase":

                if len(self.waveBoxes) > 0:
                    self.showWaveBoxes()
                else:
                    self.setUpWaveBoxes()
                    self.showWaveBoxes()
                
                self.hideEaseBoxes()
                

    
        #make view
        self.view = QtGui.QGraphicsView(self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #make view fit the widget size
        self.viewYoffset = 225
        self.view.setGeometry(0, self.viewYoffset, self.width, self.height - self.viewYoffset)

        #make scene 
        self.scene = QtGui.QGraphicsScene(self)
        #make scene fit the view size
        self.scene.setSceneRect(QtCore.QRect(0, 0, self.width, self.height))
        #set scene background colour
        self.scene.setBackgroundBrush(QtGui.QColor(0,0,0))
        #add scene to the view
        self.view.setScene(self.scene)
    
        #add lines
        self.viewTop = 115
        self.boxheight = self.height / 2
        self.boxwidth = self.width / 3
        self.line1 = lineGraphic(self, 0.0,self.boxheight,self.width,self.boxheight, QtGui.QColor(100,100,100))
        self.scene.addItem(self.line1)
        self.line2 = lineGraphic(self, self.boxwidth,self.viewTop,self.boxwidth,self.boxheight, QtGui.QColor(100,100,100))
        self.scene.addItem(self.line2)
        self.line3 = lineGraphic(self, self.boxwidth*2,self.viewTop,self.boxwidth*2,self.boxheight, QtGui.QColor(100,100,100))
        self.scene.addItem(self.line3)
        
        self.plot_yMax = self.boxheight+30.0
        self.plot_yMin = 450.0
        self.plot_xMin = 30
        self.plot_xMax = int(self.width - 30)
        
        #add start end and middle plot lines
        self.plotline1 = lineGraphic(self, self.plot_xMin,self.plot_yMin,self.plot_xMin,self.plot_yMax, QtGui.QColor(150,100,50))
        self.scene.addItem(self.plotline1)
        self.plotline2 = lineGraphic(self, self.plot_xMax,self.plot_yMin,self.plot_xMax,self.plot_yMax, QtGui.QColor(150,100,50))
        self.scene.addItem(self.plotline2)
        self.plotline3 = lineGraphic(self, self.plot_xMax,self.plot_yMin,self.plot_xMax,self.plot_yMax, QtGui.QColor(150,100,50))
        self.scene.addItem(self.plotline3)
        self.plotline3.setVisible(False)
        
        
        self.dots = []
        self.lines = []
        
        self.startDot = Particle(self,3,[0,0])
        self.startDot.move([self.plot_xMin,self.plot_yMin])
        self.startDot.setParticleColour(200,100,100)
        
        self.endDot = Particle(self,3,[0,0])
        self.endDot.move([self.plot_xMax,self.plot_yMax])
        self.endDot.setParticleColour(200,100,100)
                    
        self.curveValue = 0.0
        
        self.setFocus()

        #set up timer

        self.timer = QtCore.QBasicTimer()
        self.frameCounter = 0
        
        self.GRAPHICS_RATE = 1000 / nuke.root()['fps'].value()

        #set up animating balls

        self.slidingBall_xMin = self.boxwidth + 30.0
        self.slidingBall_xMax = (self.boxwidth*2) - 30.0
        self.slidingBall_yMin = self.viewTop + 20.0
        self.slidingBall_yMax = self.boxheight - 30.0
        
        self.slidingBall = Particle(self,8,[self.slidingBall_xMin,self.slidingBall_yMin])
        self.slidingBall.setParticleColour(100,50,50)
    
        self.growingBall_rMin = 0.05
        self.growingBall_rMax = 1.0
        self.growingBall = Particle(self,50,[0.0,0.0])
        self.growingBall.setParticleColour(100,50,50)
        self.growingBall.move([self.width/6,self.viewTop + ((self.boxheight-self.viewTop)/2)])
        
        self.flashingBall_aMin = 0.0
        self.flashingBall_aMax = 255.0
        self.flashingBall = Particle(self,50,[0.0,0.0])
        self.flashingBall.setParticleColour(0.0,0.0,0.0)
        self.flashingBall.move([(self.width/6)*5,self.viewTop + ((self.boxheight-self.viewTop)/2)])

        #set up graphics text

        self.durationText = QtGui.QGraphicsSimpleTextItem()
        if self.editMode:
            self.durationText.setText('Duration: ' + str(1 + int(self.endFrame.text()) - int(self.startFrame.text())))
        else:
            self.durationText.setText('Duration: 50')
    
        self.durationText.setPos(500,445)
        brush = QtGui.QBrush()
        brush.setColor( QtGui.QColor(200,255,200) )
        brush.setStyle( QtCore.Qt.SolidPattern )
        self.durationText.setBrush(brush)
        self.scene.addItem(self.durationText)
        
        self.fpsText = QtGui.QGraphicsSimpleTextItem()
        self.fpsText.setText('FPS: ' + '%g' % nuke.root()['fps'].value())
        self.fpsText.setPos(500,460)
        self.fpsText.setBrush(brush)
        self.scene.addItem(self.fpsText)
        
        
        self.startText = QtGui.QGraphicsSimpleTextItem()
        self.startText.setText('%g' % int(self.startFrame.text()))
        self.startText.setPos(self.plot_xMin-4,self.plot_yMax-20)
        self.startText.setBrush(brush)
        self.scene.addItem(self.startText)
    
        self.endText = QtGui.QGraphicsSimpleTextItem()
        self.endText.setText('%g' % int(self.endFrame.text()))
        self.endText.setPos(self.plot_xMax-10,self.plot_yMax-20)
        self.endText.setBrush(brush)
        self.scene.addItem(self.endText)
    
        self.midText = QtGui.QGraphicsSimpleTextItem()
        self.midText.setText('%g' % (int(self.endFrame.text())))
        self.midText.setPos((self.plot_xMax/2)+10,self.plot_yMax-20)
        self.midText.setBrush(brush)
        self.scene.addItem(self.midText)
        self.midText.setVisible(False)
    
        self.midLabelText = QtGui.QGraphicsSimpleTextItem()
        self.midLabelText.setText('ease part')
        self.midLabelText.setPos((self.plot_xMin + 100),self.plot_yMax-20)
        self.midLabelText.setBrush(brush)
        self.scene.addItem(self.midLabelText)
        self.midLabelText.setVisible(False)
    
        #create an expression from current settings and put it in the knob
        self.setTempExpressionOnKnob()
    
    
        if self.editMode and self.animType == "wave":
            #skip the animation head and go straight to main
            self.timerState = "main"
            self.slidingBall.setParticleColour(100,200,100)
            self.growingBall.setParticleColour(100,200,100)
            self.flashingBall.setParticleColour(0.0,0.0,0.0)
            self.beginAnimations()
        else:
            #start animation head
            self.startHead()

        #plot the curve in the graphics view
        self.plotCurve()
    
        self.show()
        
        
    def timerEvent(self, e):

        if self.timerState == "head":
            self.timer.stop()
            self.timerState = "main"
            self.slidingBall.setParticleColour(100,200,100)
            self.growingBall.setParticleColour(100,200,100)
            self.flashingBall.setParticleColour(0.0,0.0,0.0)
            self.beginAnimations()
        
        elif self.timerState == "main":
        
            
            #check if finished (for ease anims only)
            if (self.frameCounter >= int(self.endFrame.text())) and (self.animType == "ease"):
                self.timer.stop()
                self.startTail()
            
            else:
                
                #get the value between 0 and 1 on the temp nuke curve
                #at this time
                try:
                    curveValue = self.getCurveValueAtTime()
                except:
                    curveValue = 0
                
                
                try:
                    #animate sliding ball
                    c = float(self.slidingBall_xMax - self.slidingBall_xMin)
                    b = float(self.slidingBall_xMin)
                    x = (curveValue * c ) + b
                    c = float(self.slidingBall_yMax - self.slidingBall_yMin)
                    b = float(self.slidingBall_yMin)
                    y = (curveValue * c ) + b
                    self.slidingBall.move([x,y])
                
                    #animate growing ball
                    c = float(self.growingBall_rMax - self.growingBall_rMin)
                    b = float(self.growingBall_rMin)
                    r = (curveValue * c ) + b
                    self.growingBall.scale(r)
                    
                    #animate flashing ball
                    c = float(self.flashingBall_aMax - self.flashingBall_aMin)
                    b = float(self.flashingBall_aMin)
                    a = (curveValue * c ) + b
                    a = min(max(a,self.flashingBall_aMin),self.flashingBall_aMax) #clamp
                    self.flashingBall.fade(a)
                        
                except:
                    pass
        
    
            self.frameCounter += 1
    

        elif self.timerState == "tail":
            
            self.startHead()
    

    def startHead(self):
        #start animation head
        self.timerState = "head"
        self.slidingBall.setParticleColour(100,50,50)
        self.slidingBall.move([self.slidingBall_xMin,self.slidingBall_yMin])
        self.growingBall.setParticleColour(100,50,50)
        self.growingBall.scale(self.growingBall_rMin)
        self.flashingBall.setParticleColour(0.0,0.0,0.0)
        self.flashingBall.fade(self.flashingBall_aMin)
        
        self.timer.start(500, self)
                
    def startTail(self):
        #start animation tail
        self.timerState = "tail"
        self.slidingBall.move([self.slidingBall_xMax,self.slidingBall_yMax])
        self.growingBall.scale(self.growingBall_rMax)
        self.flashingBall.fade(self.flashingBall_aMax)
        
        self.timer.start(500, self)
    
    def beginAnimations(self):
        if self.timer.isActive():
            self.timer.stop()
        
        self.frameCounter = int(self.startFrameOld)
        self.duration = 1 + int(self.endFrameOld) - int(self.startFrameOld) #in fps
        self.timer.start(self.GRAPHICS_RATE, self)



    def createControlsForKnob(self):
        
        #create a new tab for this knob with all the knobs on the node in question
        theTab = nuke.Tab_Knob("anim_tab_" + self.theKnobName, self.theKnobName + " anim")
        self.theNode.addKnob(theTab)
        
        #make ease controls
        
        easeType = nuke.Text_Knob('a_easeType_display_' + self.theKnobName,'Animation type:')
        easeType.setValue('Linear')
        self.theNode.addKnob(easeType)
        
        startFrame = nuke.Int_Knob('a_startFrame_' + self.theKnobName,'Start Frame:')
        startFrame.setValue(1)
        self.theNode.addKnob(startFrame)
        
        endFrame = nuke.Int_Knob('a_endFrame_' + self.theKnobName,'End Frame:')
        endFrame.setValue(50)
        self.theNode.addKnob(endFrame)
        
        startValue = nuke.Double_Knob('a_startValue_' + self.theKnobName,'Start Value:')
        startValue.setValue(0.0)
        self.theNode.addKnob(startValue)
        
        endValue = nuke.Double_Knob('a_endValue_' + self.theKnobName,'End Value:')
        endValue.setValue(10.0)
        self.theNode.addKnob(endValue)
        
        easeTypeHidden = nuke.Text_Knob('a_easeType_' + self.theKnobName,'Ease type:')
        easeTypeHidden.setValue('Linear')
        easeTypeHidden.setVisible(False)
        self.theNode.addKnob(easeTypeHidden)
        
        #make wave controls
        
        waveType = nuke.Text_Knob('a_waveType_display_' + self.theKnobName,'Animation type:')
        waveType.setValue('Sine')
        self.theNode.addKnob(waveType)
        
        minValue = nuke.Double_Knob('a_minValue_' + self.theKnobName,'Min Value:')
        minValue.setValue(0.0)
        self.theNode.addKnob(minValue)
        
        maxValue = nuke.Double_Knob('a_maxValue_' + self.theKnobName,'Max Value:')
        maxValue.setValue(1.0)
        self.theNode.addKnob(maxValue)
        
        wavelength = nuke.Double_Knob('a_wavelength_' + self.theKnobName,'Wavelength:')
        wavelength.setValue(100.0)
        self.theNode.addKnob(wavelength)
        
        offset = nuke.Double_Knob('a_offset_' + self.theKnobName,'Offset:')
        offset.setValue(0.0)
        self.theNode.addKnob(offset)
        
        bcutoff = nuke.Double_Knob('a_bcutoff_' + self.theKnobName,'Blip cutoff:')
        bcutoff.setValue(0.95)
        self.theNode.addKnob(bcutoff)
        
        waveTypeHidden = nuke.Text_Knob('a_waveType_' + self.theKnobName,'Wave type:')
        waveTypeHidden.setValue('Sine')
        waveTypeHidden.setVisible(False)
        self.theNode.addKnob(waveTypeHidden)
        
        #add edit button, hard coded to load settings for this tab's related knob
        editButton = nuke.PyScript_Knob('a_edit_' + self.theKnobName,'EDIT')
        editButton.setValue("AnimationMaker.showWindow('%s',%s)" %(self.origKnobName,self.knobIndex))
        editButton.clearFlag(nuke.STARTLINE)
        self.theNode.addKnob(editButton)
        




    def closeButtonPressed(self):
        
        theNodeKnobs = self.theNode.knobs()
        
        #check if this particular node already has an animation maker tab
        #create tab and control knobs if not
        if not ("anim_tab_%s" % (self.theKnobName) in theNodeKnobs):
            self.createControlsForKnob()
        
        if self.animType == "ease" or self.animType == "waveEase":
            
            self.showEaseKnobs()
            
            #hide wave knobs if exist (for ease only)
            if self.animType == "ease":
                self.hideWaveKnobs()
            
            startValueFloat = float(self.startValue.text())
            endValueFloat = float(self.endValue.text())
            rangeFloat = endValueFloat-startValueFloat
            
            #update the existing ease knobs on the node
            self.theNode['a_startFrame_' + self.theKnobName].setValue(int(self.startFrame.text()))
            self.theNode['a_endFrame_' + self.theKnobName].setValue(int(self.endFrame.text()))
            self.theNode['a_startValue_' + self.theKnobName].setValue(startValueFloat)
            self.theNode['a_startValue_' + self.theKnobName].setRange(startValueFloat-(rangeFloat/4),endValueFloat)
            self.theNode['a_endValue_' + self.theKnobName].setValue(endValueFloat)
            self.theNode['a_endValue_' + self.theKnobName].setRange(startValueFloat , endValueFloat+(rangeFloat/4))
            self.theNode['a_easeType_' + self.theKnobName].setValue(str(self.easeType.currentText()))
            self.theNode['a_easeType_display_' + self.theKnobName].setValue("<h3><font color='yellow'>EASE </font><font color='white'>" + str(self.easeType.currentText()) + "</font></h3>")

            if self.animType == "waveEase":
                self.theNode['a_startValue_' + self.theKnobName].setVisible(False)
                self.theNode['a_endValue_' + self.theKnobName].setVisible(False)
            else:
                self.theNode['a_startValue_' + self.theKnobName].setVisible(True)
                self.theNode['a_endValue_' + self.theKnobName].setVisible(True)
            

                
        if self.animType == "wave" or self.animType == "waveEase":
            
            self.showWaveKnobs()
            
            #hide the ease controls if exist (for wave only)
            if self.animType == "wave":
                self.hideEaseKnobs()
                    
            minValueFloat = float(self.minValue.text())
            maxValueFloat = float(self.maxValue.text())
            wavelengthFloat = float(self.wavelength.text())
            offsetFloat = float(self.offset.text())
            bcutoffFloat = float(self.bcutoff.text())
            rangeFloat = maxValueFloat-minValueFloat
            
                
            #update the existing wave knobs on the node
            self.theNode['a_minValue_' + self.theKnobName].setValue(minValueFloat)
            self.theNode['a_minValue_' + self.theKnobName].setRange(minValueFloat-(rangeFloat/4),maxValueFloat)
            self.theNode['a_maxValue_' + self.theKnobName].setValue(maxValueFloat)
            self.theNode['a_maxValue_' + self.theKnobName].setRange(minValueFloat , maxValueFloat+(rangeFloat/4))
            
            self.theNode['a_wavelength_' + self.theKnobName].setValue(wavelengthFloat)
            self.theNode['a_wavelength_' + self.theKnobName].setRange(wavelengthFloat -(wavelengthFloat/4) , wavelengthFloat +(wavelengthFloat*4))
            self.theNode['a_offset_' + self.theKnobName].setValue(offsetFloat)
            self.theNode['a_offset_' + self.theKnobName].setRange(offsetFloat -(offsetFloat* 0.25) -10 , offsetFloat +(offsetFloat*4)+10)
            
            self.theNode['a_bcutoff_' + self.theKnobName].setValue(bcutoffFloat)
            self.theNode['a_bcutoff_' + self.theKnobName].setRange(0.0,1.0)
            if self.blip.isChecked():
                self.theNode['a_bcutoff_' + self.theKnobName].setVisible(True)
            else:
                self.theNode['a_bcutoff_' + self.theKnobName].setVisible(False)
            
            self.theNode['a_waveType_' + self.theKnobName].setValue(str(self.waveType.currentText()))
            if self.squarifyOld == True:
                self.theNode['a_waveType_display_' + self.theKnobName].setValue("<h3><font color='yellow'>WAVE </font><font color='white'>" + str(self.waveType.currentText()) + " (squared)</font></h3>")
            elif self.blipOld == True:
                self.theNode['a_waveType_display_' + self.theKnobName].setValue("<h3><font color='yellow'>WAVE </font><font color='white'>" + str(self.waveType.currentText()) + " (blip)</font></h3>")
            else:
                self.theNode['a_waveType_display_' + self.theKnobName].setValue("<h3><font color='yellow'>WAVE </font><font color='white'>" + str(self.waveType.currentText()) + "</font></h3>")
            


        #make or set the hidden animType knob
        if "a_animType_%s" % (self.theKnobName) in theNodeKnobs:
            self.theNode['a_animType_' + self.theKnobName].setValue(self.animType)
        else:
            animTypeHidden = nuke.Text_Knob('a_animType_' + self.theKnobName,'Anim type:')
            animTypeHidden.setValue(self.animType)
            animTypeHidden.setVisible(False)
            self.theNode.addKnob(animTypeHidden)


        if self.animType == "ease":
            #generate the tcl version of the expression
            self.theExpression = self.getEaseExpression(False)
        elif self.animType == "wave":
            #generate the tcl version of the expression linking to the node user knobs
            self.theExpression = self.getWaveExpression(False)
        elif self.animType == "waveEase":
            #generate the tcl version of the expression
            self.theExpression = self.getWaveEaseExpression(False)

                    
                    
        #add the tcl expression to the relevant knob
                    
        if self.knobIndex > -1:
            self.theKnob.setExpression(self.theExpression,self.knobIndex)
        else:
            self.theKnob.setExpression(self.theExpression)


        self.updateCreateButtonPressed = True
        self.close()
        
        
    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        

        if not self.updateCreateButtonPressed:
                #copy the original value, keyframes or expression back
                self.theKnob.clearAnimated()
                self.theKnob.fromScript(self.originalValue)


    def easeButtonPressed(self):
        
        self.waveButton.setStyleSheet('')
        self.easeButton.setStyleSheet('QWidget { background-color: #115511 }')
        
        if len(self.waveBoxes) > 0:
            self.hideWaveBoxes()
        
        self.showEaseBoxes()
                
        self.animType = "ease"
        self.setTempExpressionOnKnob()
        
        self.plotCurve()


    def waveButtonPressed(self):
        
        self.easeButton.setStyleSheet('')
        self.waveButton.setStyleSheet('QWidget { background-color: #115511 }')
        
        self.hideEaseBoxes()
        if len(self.waveBoxes) > 0:
            self.showWaveBoxes()
        else:
            self.setUpWaveBoxes()
            self.showWaveBoxes()

        try:
            if self.waveEase.isChecked():
                self.animType = "waveEase"
            else:
                self.animType = "wave"
        except:
            pass

        self.setTempExpressionOnKnob()
        
        #plot the new curve
        self.plotCurve()
                
        self.timer.stop()
        self.timerState = "main"
        self.slidingBall.setParticleColour(100,200,100)
        self.growingBall.setParticleColour(100,200,100)
        self.flashingBall.setParticleColour(0.0,0.0,0.0)
        self.beginAnimations()




            
            
    def setUpEaseBoxes(self):
    
        rowSpacing = 40
        inputsLeft = 230
        
        #make input boxes
        self.startFrameLabel = QtGui.QLabel(self)
        self.startFrameLabel.setText('Start Frame')
        self.startFrameLabel.move(inputsLeft, 10)
        self.startFrame = QtGui.QLineEdit(self)
        self.startFrame.move(inputsLeft, 10+15)
        if self.editMode:
            try:
                self.startFrame.setText(str(self.theNode['a_startFrame_'+self.theKnobName].value()))
            except:
                self.startFrame.setText('1')
        else:
            self.startFrame.setText('1')
        self.startFrame.editingFinished.connect(self.userValuesChanged)
        self.startFrameOld = self.startFrame.text()
        self.easeBoxes.append(self.startFrameLabel)
        self.easeBoxes.append(self.startFrame)
        
        self.endFrameLabel = QtGui.QLabel(self)
        self.endFrameLabel.setText('End Frame')
        self.endFrameLabel.move(inputsLeft, rowSpacing*1.3)
        self.endFrame = QtGui.QLineEdit(self)
        self.endFrame.move(inputsLeft, rowSpacing*1.3+15)
        if self.editMode:
            try:
                self.endFrame.setText(str(self.theNode['a_endFrame_'+self.theKnobName].value()))
            except:
                self.endFrame.setText('50')
        else:
            self.endFrame.setText('50')
        self.endFrame.editingFinished.connect(self.userValuesChanged)
        self.endFrameOld = self.endFrame.text()
        self.easeBoxes.append(self.endFrameLabel)
        self.easeBoxes.append(self.endFrame)

        self.startValueLabel = QtGui.QLabel(self)
        self.startValueLabel.setText('Start Value')
        self.startValueLabel.move(inputsLeft, rowSpacing*2.3)
        self.startValue = QtGui.QLineEdit(self)
        self.startValue.move(inputsLeft, rowSpacing*2.3+15)
        if self.editMode:
            try:
                self.startValue.setText( '%g' % self.theNode['a_startValue_'+self.theKnobName].value()  )
            except:
                self.startValue.setText('0')
        else:
            self.startValue.setText('0')
        self.startValue.editingFinished.connect(self.userValuesChanged)
        self.startValueOld = self.startValue.text()
        self.easeBoxes.append(self.startValueLabel)
        self.easeBoxes.append(self.startValue)
        
        self.endValueLabel = QtGui.QLabel(self)
        self.endValueLabel.setText('End Value')
        self.endValueLabel.move(inputsLeft, rowSpacing*3.3)
        self.endValue = QtGui.QLineEdit(self)
        self.endValue.move(inputsLeft, rowSpacing*3.3+15)
        if self.editMode:
            try:
                self.endValue.setText('%g' % self.theNode['a_endValue_'+self.theKnobName].value())
            except:
                self.endValue.setText('10')
        else:
            self.endValue.setText('10')
        self.endValue.editingFinished.connect(self.userValuesChanged)
        self.endValueOld = self.endValue.text()
        self.easeBoxes.append(self.endValueLabel)
        self.easeBoxes.append(self.endValue)

        self.easeTypeLabel = QtGui.QLabel(self)
        self.easeTypeLabel.setText('Ease Type')
        self.easeTypeLabel.move(inputsLeft, rowSpacing*4.3)
        self.easeType = QtGui.QComboBox(self)
        self.easeType.addItems(["Linear","Quad Ease IN","Quad Ease OUT","Quad Ease IN & OUT","Expo Ease IN","Expo Ease OUT","Expo Ease IN & OUT","Ease OUT & BACK", "Ease OUT Bounce", "Ease OUT Elastic"])
        self.easeType.move(inputsLeft, rowSpacing*4.3+15)
        if self.editMode:
            try:
                theIndex = self.easeType.findText(self.theNode['a_easeType_'+self.theKnobName].value(),QtCore.Qt.MatchExactly)
                self.easeType.setCurrentIndex(theIndex)
            except:
                pass
        self.easeType.currentIndexChanged.connect(self.userValuesChanged)
        self.easeTypeOld = self.easeType.currentIndex()
        self.easeBoxes.append(self.easeTypeLabel)
        self.easeBoxes.append(self.easeType)


    def hideEaseBoxes(self):
        for e in self.easeBoxes:
            e.setVisible(False)

    def showEaseBoxes(self):
        for e in self.easeBoxes:
            e.setVisible(True)

    def hideEaseKnobs(self):
        self.theNode['a_startFrame_' + self.theKnobName].setVisible(False)
        self.theNode['a_endFrame_' + self.theKnobName].setVisible(False)
        self.theNode['a_startValue_' + self.theKnobName].setVisible(False)
        self.theNode['a_endValue_' + self.theKnobName].setVisible(False)
        self.theNode['a_easeType_' + self.theKnobName].setVisible(False)
        self.theNode['a_easeType_display_' + self.theKnobName].setVisible(False)

    def showEaseKnobs(self):
        self.theNode['a_startFrame_' + self.theKnobName].setVisible(True)
        self.theNode['a_endFrame_' + self.theKnobName].setVisible(True)
        self.theNode['a_startValue_' + self.theKnobName].setVisible(True)
        self.theNode['a_endValue_' + self.theKnobName].setVisible(True)
        self.theNode['a_easeType_display_' + self.theKnobName].setVisible(True)

    
    def setUpWaveBoxes(self):
        
        rowSpacing = 40
        inputsLeft = 230
        
        #make input boxes
        self.minValueLabel = QtGui.QLabel(self)
        self.minValueLabel.setText('Min value')
        self.minValueLabel.move(inputsLeft, 10)
        self.minValue = QtGui.QLineEdit(self)
        self.minValue.move(inputsLeft, 10+15)
        if self.editMode:
            try:
                self.minValue.setText('%g' % self.theNode['a_minValue_'+self.theKnobName].value())
            except:
                
                self.minValue.setText('0')
        else:
            self.minValue.setText('0')

        self.minValue.editingFinished.connect(self.userValuesChanged)
        self.minValueOld = self.minValue.text()
        self.waveBoxes.append(self.minValueLabel)
        self.waveBoxes.append(self.minValue)
        
        self.maxValueLabel = QtGui.QLabel(self)
        self.maxValueLabel.setText('Max value')
        self.maxValueLabel.move(inputsLeft, rowSpacing*1.3)
        self.maxValue = QtGui.QLineEdit(self)
        self.maxValue.move(inputsLeft, rowSpacing*1.3+15)
        if self.editMode:
            try:
                self.maxValue.setText('%g' % self.theNode['a_maxValue_'+self.theKnobName].value())
            except:
                self.maxValue.setText('1')
        else:
            self.maxValue.setText('1')

        self.maxValue.editingFinished.connect(self.userValuesChanged)
        self.maxValueOld = self.maxValue.text()
        self.waveBoxes.append(self.maxValueLabel)
        self.waveBoxes.append(self.maxValue)
        
        self.wavelengthLabel = QtGui.QLabel(self)
        self.wavelengthLabel.setText('Wavelength')
        self.wavelengthLabel.move(inputsLeft, rowSpacing*2.3)
        self.wavelength = QtGui.QLineEdit(self)
        self.wavelength.move(inputsLeft, rowSpacing*2.3+15)
        if self.editMode:
            try:
                self.wavelength.setText('%g' % self.theNode['a_wavelength_'+self.theKnobName].value())
            except:
                self.wavelength.setText('100')
        else:
            self.wavelength.setText('100')
        
        self.wavelength.editingFinished.connect(self.userValuesChanged)
        self.wavelengthOld = self.wavelength.text()
        self.waveBoxes.append(self.wavelengthLabel)
        self.waveBoxes.append(self.wavelength)
        
        self.offsetLabel = QtGui.QLabel(self)
        self.offsetLabel.setText('Offset')
        self.offsetLabel.move(inputsLeft, rowSpacing*3.3)
        self.offset = QtGui.QLineEdit(self)
        self.offset.move(inputsLeft, rowSpacing*3.3+15)
        if self.editMode:
            try:
                self.offset.setText('%g' % self.theNode['a_offset_'+self.theKnobName].value())
            except:
                self.offset.setText('0')
        else:
            self.offset.setText('0')
        
        self.offset.editingFinished.connect(self.userValuesChanged)
        self.offsetOld = self.offset.text()
        self.waveBoxes.append(self.offsetLabel)
        self.waveBoxes.append(self.offset)
        
        self.waveTypeLabel = QtGui.QLabel(self)
        self.waveTypeLabel.setText('Wave Type')
        self.waveTypeLabel.move(inputsLeft, rowSpacing*4.3)
        self.waveType = QtGui.QComboBox(self)
        self.waveType.addItems(["Sine","Random","Noise","Triangle","Sawtooth","Sawtooth Curved","Sawtooth Curved Rev.","Sawtooth Exponential","Bounce"])
        self.waveType.move(inputsLeft, rowSpacing*4.3+15)
        if self.editMode:
            try:
                theIndex = self.waveType.findText(self.theNode['a_waveType_'+self.theKnobName].value(),QtCore.Qt.MatchExactly)
                self.waveType.setCurrentIndex(theIndex)
            except:
                pass
                    
        self.waveType.currentIndexChanged.connect(self.userValuesChanged)
        self.waveTypeOld = self.waveType.currentIndex()
        self.waveBoxes.append(self.waveTypeLabel)
        self.waveBoxes.append(self.waveType)


        #radio buttons
        self.radioGroup = QtGui.QGroupBox(self)
        self.radioGroup.setGeometry(inputsLeft+150, 26,200,134)
        self.waveBoxes.append(self.radioGroup)
        
        self.normalWave = QtGui.QRadioButton('Normal wave',self.radioGroup)
        self.normalWave.move(10, 10)
        self.normalWave.setChecked(True)
        self.waveBoxes.append(self.normalWave)
        
        self.waveEase = QtGui.QRadioButton('Combine with ease curve',self.radioGroup)
        self.waveEase.move(10, 40)
        self.waveEase.setChecked(False)
        self.waveEaseOld = False
        if self.editMode:
            try:
                if self.theNode['a_animType_'+self.theKnobName].value() == "waveEase":
                    self.waveEase.setChecked(True)
                    self.waveEaseOld = True
            except:
                pass

        self.waveEase.toggled.connect(self.userValuesChanged)
        self.waveBoxes.append(self.waveEase)
        
        self.squarify = QtGui.QRadioButton('Squarify',self.radioGroup)
        self.squarify.move(10, 70)
        self.squarify.setChecked(False)
        self.squarifyOld = False
        if self.editMode:
            try:
                if "squared" in self.theNode['a_waveType_display_' + self.theKnobName].value():
                    self.squarify.setChecked(True)
                    self.squarifyOld = True
            except:
                pass

        self.squarify.toggled.connect(self.userValuesChanged)
        self.waveBoxes.append(self.squarify)
        
        self.blip = QtGui.QRadioButton('Blip',self.radioGroup)
        self.blip.move(10, 100)
        self.blip.setChecked(False)
        self.blipOld = False
        if self.editMode:
            try:
                if "blip" in self.theNode['a_waveType_display_' + self.theKnobName].value():
                    self.blip.setChecked(True)
                    self.blipOld = True
            except:
                pass

        self.blip.toggled.connect(self.userValuesChanged)
        self.waveBoxes.append(self.blip)

        self.bcutoffLabel = QtGui.QLabel(self)
        self.bcutoffLabel.setText('cutoff')
        self.bcutoffLabel.move(520, 128)
        self.bcutoff = QtGui.QLineEdit(self)
        self.bcutoff.setGeometry(445, 126, 68, 20)


        if self.editMode:
            try:
                self.bcutoff.setText('%g' % self.theNode['a_bcutoff_'+self.theKnobName].value())
            except:
                self.bcutoff.setText('0.95')
        else:
            self.bcutoff.setText('0.95')
        
        self.bcutoff.editingFinished.connect(self.userValuesChanged)
        self.bcutoffOld = self.bcutoff.text()
        self.waveBoxes.append(self.bcutoffLabel)
        self.waveBoxes.append(self.bcutoff)



    def hideWaveBoxes(self):
        for w in self.waveBoxes:
            w.setVisible(False)
    
    def showWaveBoxes(self):
        for w in self.waveBoxes:
            w.setVisible(True)

        self.bcutoffLabel.setVisible(self.blip.isChecked())
        self.bcutoff.setVisible(self.blip.isChecked())


    def hideWaveKnobs(self):
        self.theNode['a_minValue_' + self.theKnobName].setVisible(False)
        self.theNode['a_maxValue_' + self.theKnobName].setVisible(False)
        self.theNode['a_wavelength_' + self.theKnobName].setVisible(False)
        self.theNode['a_offset_' + self.theKnobName].setVisible(False)
        self.theNode['a_waveType_' + self.theKnobName].setVisible(False)
        self.theNode['a_waveType_display_' + self.theKnobName].setVisible(False)
        self.theNode['a_bcutoff_' + self.theKnobName].setVisible(False)

    def showWaveKnobs(self):
        self.theNode['a_minValue_' + self.theKnobName].setVisible(True)
        self.theNode['a_maxValue_' + self.theKnobName].setVisible(True)
        self.theNode['a_wavelength_' + self.theKnobName].setVisible(True)
        self.theNode['a_offset_' + self.theKnobName].setVisible(True)
        self.theNode['a_waveType_display_' + self.theKnobName].setVisible(True)



    def userValuesChanged(self):
        if self.checkForChangedValues():
            self.duration = 1 + int(self.endFrame.text()) - int(self.startFrame.text())
            self.durationText.setText("Duration: " + str(self.duration))
            if self.animType == "wave" or self.animType == "waveEase":
                try:
                    if self.waveEase.isChecked():
                        self.animType = "waveEase"
                    else:
                        self.animType = "wave"
                except:
                    pass
            
            self.setTempExpressionOnKnob()
            
            if self.animType == "ease" or self.animType == "waveEase":
                #start animation head
                self.startHead()
            elif self.animType == "wave":
                self.timer.stop()
                self.timerState = "main"
                self.slidingBall.setParticleColour(100,200,100)
                self.growingBall.setParticleColour(100,200,100)
                self.flashingBall.setParticleColour(0.0,0.0,0.0)
                self.beginAnimations()
    
            #plot the new curve
            self.plotCurve()


    def checkForChangedValues(self):
        hasChanged = False
        
        if self.animType == "ease":
            
            if self.startFrame.text() != self.startFrameOld:
                self.startFrameOld = self.startFrame.text()
                hasChanged = True
            
            if self.endFrame.text() != self.endFrameOld:
                self.endFrameOld = self.endFrame.text()
                hasChanged = True
            
            if self.startValue.text() != self.startValueOld:
                self.startValueOld = self.startValue.text()
                hasChanged = True
            
            if self.endValue.text() != self.endValueOld:
                self.endValueOld = self.endValue.text()
                hasChanged = True
            
            if self.easeType.currentIndex() != self.easeTypeOld:
                self.easeTypeOld = self.easeType.currentIndex()
                hasChanged = True
        
        elif self.animType == "wave" or self.animType == "waveEase":
            
            if self.minValue.text() != self.minValueOld:
                self.minValueOld = self.minValue.text()
                hasChanged = True
            
            if self.maxValue.text() != self.maxValueOld:
                self.maxValueOld = self.maxValue.text()
                hasChanged = True
            
            if self.wavelength.text() != self.wavelengthOld:
                self.wavelengthOld = self.wavelength.text()
                hasChanged = True
            
            if self.offset.text() != self.offsetOld:
                self.offsetOld = self.offset.text()
                hasChanged = True
            
            try:
                if self.bcutoff.text() != self.bcutoffOld:
                    self.bcutoffOld = self.bcutoff.text()
                    hasChanged = True
            except:
                pass
            
            if self.waveType.currentIndex() != self.waveTypeOld:
                self.waveTypeOld = self.waveType.currentIndex()
                hasChanged = True
            
            try:
                if self.waveEase.isChecked() != self.waveEaseOld:
                    self.waveEaseOld = self.waveEase.isChecked()
                    hasChanged = True
            except:
                pass
                    
            try:
                if self.squarify.isChecked() != self.squarifyOld:
                    self.squarifyOld = self.squarify.isChecked()
                    hasChanged = True
            except:
                pass
                    
            try:
                if self.blip.isChecked() != self.blipOld:
                    self.blipOld = self.blip.isChecked()
                    if self.blipOld == True:
                        self.bcutoffLabel.setVisible(True)
                        self.bcutoff.setVisible(True)
                    else:
                        self.bcutoffLabel.setVisible(False)
                        self.bcutoff.setVisible(False)
                    
                    hasChanged = True
            except:
                pass
    
    
    
        return hasChanged


    def setTempExpressionOnKnob(self):
        
        #generate the tcl version of the expression
        if self.animType == "ease":
            self.theExpression = self.getEaseExpression(True)
        
        elif self.animType == "wave":
            self.theExpression = self.getWaveExpression(True)

        elif self.animType == "waveEase":
            self.theExpression = self.getWaveEaseExpression(True)
                
        
        #add the tcl expression to the relevant knob
        if self.knobIndex > -1 and (self.knobAmount > 1) == True:
            self.theKnob.setExpression(self.theExpression,self.knobIndex)
        else:
            self.theKnob.setExpression(self.theExpression)

                
            
    
    def plotCurve(self):
        
        index = 0
        
        c = float(self.plot_yMax - self.plot_yMin)
        b = float(self.plot_yMin)
        
    
        if len(self.dots)>0:
            dotsExist = True
        else:
            dotsExist = False


        self.plotline3.setVisible(False)
        self.midText.setVisible(False)
        self.midLabelText.setVisible(False)

        if self.animType == "ease" or self.animType == "waveEase":
            
            self.startDot.graphic.setVisible(True)
            self.endDot.graphic.setVisible(True)
            self.durationText.setVisible(True)
            
            start = float(self.startFrameOld)
            end = float(self.endFrameOld)
            
            
            if self.animType == "waveEase":
                self.startDot.move([self.plot_xMin,self.plot_yMin])
                self.endDot.move([(self.plot_xMax+self.plot_xMin)/2,self.plot_yMax])
                self.plotline3.setLine((self.plot_xMax+self.plot_xMin)/2,self.plot_yMin,(self.plot_xMax+self.plot_xMin)/2,self.plot_yMax)
                self.plotline3.setVisible(True)
                self.midText.setVisible(True)
                self.midLabelText.setVisible(True)
                self.startText.setText('%g' % int(self.startFrame.text()))
                self.midText.setText('%g' % (int(self.endFrame.text())))
                
                end += (end-start) #show more at the end of the ease
                self.endText.setText('%g' % int(end))
                
            elif self.animType == "ease":
                self.startDot.move([self.plot_xMin,self.plot_yMin])
                self.endDot.move([self.plot_xMax,self.plot_yMax])
                self.startText.setText('%g' % int(self.startFrame.text()))
                self.endText.setText('%g' % (int(self.endFrame.text())))
            
            
            curveDuration = end-start
            
            

            plotWidth = float(self.plot_xMax - self.plot_xMin)
            incAmount = curveDuration / plotWidth
            
            
            for xVal in floatRange(start,end,incAmount):
                
                try:
                    yVal = self.getCurveValueAtTime(True,xVal)
                except:
                    yVal = 0
                
                fractionAlong = ((xVal - start) / curveDuration)
                plotX = (plotWidth * fractionAlong) + self.plot_xMin
                try:
                    plotY = (yVal * c ) + b
                except:
                    plotY = 0
                            
                if not dotsExist:
                    self.dots.append(Particle(self,1,[0,0]))
                
                self.dots[index].setParticleColour(100,200,100)
                self.dots[index].move([plotX,plotY])
                
                if self.animType == "waveEase":
                    #colour ease part differently
                    if xVal <= (curveDuration/2)+0.5:
                        self.dots[index].setParticleColour(200,100,100)
                
                
                #add line joining this one to the last dot
                if index>0:
                    if not dotsExist:
                        theLine = QtGui.QGraphicsLineItem(plotX,plotY,self.dots[index-1].pos[0],self.dots[index-1].pos[1])
                        theLine.setPen(QtGui.QPen(QtGui.QColor(200,200,200)))
                        self.lines.append(theLine)
                        self.scene.addItem(theLine)
                    else:
                        self.lines[index-1].setLine(plotX,plotY,self.dots[index-1].pos[0],self.dots[index-1].pos[1])
                                    
                index +=1

        elif self.animType == "wave":
            
            self.startDot.graphic.setVisible(False)
            self.endDot.graphic.setVisible(False)
            self.durationText.setVisible(False)
            self.startText.setText('%g' % int(self.plot_xMin-30))
            self.endText.setText('%g' % (int(self.plot_xMax-29)))
            
            for plotX in range(self.plot_xMin,self.plot_xMax+1):
                try:
                    plotY = self.getCurveValueAtTime(True,plotX - self.plot_xMin)
                except:
                    plotY = 0
                
                try:
                    plotY = (plotY * c ) + b
                except:
                    plotY = 0
                    
                if not dotsExist:
                    self.dots.append(Particle(self,1,[0,0]))


                self.dots[index].setParticleColour(100,200,100)
                self.dots[index].move([plotX,plotY])

                #add line joining this one to the last dot
                if index>0:
                    if not dotsExist:
                        theLine = QtGui.QGraphicsLineItem(plotX,plotY,self.dots[index-1].pos[0],self.dots[index-1].pos[1])
                        theLine.setPen(QtGui.QPen(QtGui.QColor(200,200,200)))
                        self.lines.append(theLine)
                        self.scene.addItem(theLine)
                    else:
                        self.lines[index-1].setLine(plotX,plotY,self.dots[index-1].pos[0],self.dots[index-1].pos[1])

                index +=1






    def getCurveValueAtTime(self,plot = None,plotTime = 0):
        
        if plot:
            t = float(plotTime)
        else:
            t = self.frameCounter
            
        #get the value at current time from the expression on the node itself
        try:
            curveValue = self.theNode[self.theKnobName].getValueAt(t)
        except:
            try:
                if self.knobIndex > -1:
                    curveValue = self.theKnob.getValueAt(t,self.knobIndex)
                else:
                    curveValue = self.theKnob.getValueAt(t,0)
            except:
                curveValue = 0

        return curveValue
        
        


    def getEaseExpression(self,forPanel = False):
        
        theEaseType = str(self.easeType.currentText())
        
        if forPanel == True:
            #generate a normalized nuke expression from which to read the curve values
            #when animating things in the panel
            
            c = "1"
            b = "0"
            
            t = "(frame - %s)" % (self.startFrameOld)
            d = "(%s - %s)" % (self.endFrameOld,self.startFrameOld)
            
           
            td = "(%s / %s)" % (t,d)
            td2 = "(%s / (%s / 2))" % (t,d)
        
            easePrefix = "frame < %s ? 0 : frame > %s ? 1 : " % (self.startFrameOld,self.endFrameOld)
                
                
        else:
        
            #generate nuke expression based on the values chosen
            
            if self.animType == "waveEase":
                c = "1"
                b = "0"
                easePrefix = "frame < a_startFrame_%s ? 0 : frame > a_endFrame_%s ? 1 : " % (self.theKnobName,self.theKnobName)
            else:
                easePrefix = "frame < a_startFrame_%s ? a_startValue_%s : frame > a_endFrame_%s ? a_endValue_%s : " % (self.theKnobName,self.theKnobName,self.theKnobName,self.theKnobName)
                c = "(a_endValue_%s - a_startValue_%s)" % (self.theKnobName,self.theKnobName)
                b = "a_startValue_%s" % (self.theKnobName)
                
            t = "(frame - a_startFrame_%s)" % (self.theKnobName)
            d = "(a_endFrame_%s - a_startFrame_%s)" % (self.theKnobName,self.theKnobName)
            td = "((frame - a_startFrame_%s) / (a_endFrame_%s - a_startFrame_%s))" % (self.theKnobName,self.theKnobName,self.theKnobName)
            td2 = "((frame - a_startFrame_%s) / ((a_endFrame_%s - a_startFrame_%s) / 2))" % (self.theKnobName,self.theKnobName,self.theKnobName)
        
                
                
        if theEaseType == "Linear":
            #c * t / d + b
            return easePrefix + "%s * %s / %s + %s" %(c,t,d,b)
        
        elif theEaseType == "Quad Ease IN":
            #c * td * td + b
            return easePrefix + "%s * %s * %s + %s" %(c,td,td,b)
        
        elif theEaseType == "Quad Ease OUT":
            #-c * td * (td-2) + b
            return easePrefix + "-%s * %s * (%s-2) + %s" %(c,td,td,b)
        
        elif theEaseType == "Quad Ease IN & OUT":
            #(td2 < 1 ? c/2*td2*td2 + b : -c/2 * ((td2-1)*((td2-1)-2) - 1) + b)
            return easePrefix + "(%s < 1 ? %s/2 * %s * %s + %s : -%s/2 * ((%s-1)*((%s-1)-2) - 1) + %s)" %(td2,c,td2,td2,b,c,td2,td2,b)

        elif theEaseType == "Expo Ease IN":
            #c * (2 ** (10 * (td - 1)) ) + b
            return easePrefix + "%s * (2 ** (10 * (%s - 1)) ) + %s" %(c,td,b)

        elif theEaseType == "Expo Ease OUT":
            #c * ( -( 2**(-10 * t/d) ) + 1 ) + b
            return easePrefix + "%s * ( -( 2**(-10 * %s) ) + 1 ) + %s" %(c,td,b)

        elif theEaseType == "Expo Ease IN & OUT":
            #td2 < 1 ? c / 2 * (2 ** (10 * (td2 - 1)) ) + b : c / 2 * (-(2 ** (-10 * (td2-1))) + 2) + b
            return easePrefix + "%s < 1 ? %s / 2 * (2 ** (10 * (%s - 1)) ) + %s : %s / 2 * (-(2 ** (-10 * (%s-1))) + 2) + %s" %(td2,c,td2,b,c,td2,b)

        elif theEaseType == "Ease OUT & BACK":
            #s = 1.70158
            #c * ((t/d-1)*(t/d-1)*((s+1)*(t/d-1) + s) + 1) + b
            return easePrefix + "%s * ((%s/%s-1)*(%s/%s-1)*((%s+1)*(%s/%s-1) + %s) + 1) + %s" %(c,t,d,t,d,1.70158,t,d,1.70158,b)

        elif theEaseType == "Ease OUT Bounce":
            #td < (1/2.75) ? c * (7.5625 * td * td) + b : td < (2/2.75) ? c * (7.5625 * (td - (1.5/2.75)) * (td - (1.5/2.75)) + 0.75) + b :        td < (2.5/2.75) ? c * (7.5625 * (td - (2.25/2.75)) * (td - (2.25/2.75)) + 0.9375) + b : c * (7.5625 * (td - (2.625/2.75)) * (td - (2.625/2.75)) + 0.984375) + b

            return easePrefix + "%s < (1/2.75) ? %s * (7.5625 * %s * %s) + %s : %s < (2/2.75) ? %s * (7.5625 * (%s - (1.5/2.75)) * (%s - (1.5/2.75)) + 0.75) + %s :        %s < (2.5/2.75) ? %s * (7.5625 * (%s - (2.25/2.75)) * (%s - (2.25/2.75)) + 0.9375) + %s : %s * (7.5625 * (%s - (2.625/2.75)) * (%s - (2.625/2.75)) + 0.984375) + %s" %(td,c,td,td,b,td,c,td,td,b,td,c,td,td,b,c,td,td,b)


        elif theEaseType == "Ease OUT Elastic":
            
            #c * (2**(-10 * td)) * sin( (td * d-((d * 0.3) / 4)) * (3.14159 * 2) / (d * 0.3) ) + c + b
            return easePrefix + "%s * (2**(-10 * %s)) * sin( (%s * %s-((%s * 0.3) / 4)) * (3.14159 * 2) / (%s * 0.3) ) + %s + %s" %(c,td,td,d,d,d,c,b)




    def getWaveExpression(self, forPanel = False, easeExpression = None):
        
        #generate nuke expression based on the values chosen
        
        theWaveType = str(self.waveType.currentText())
        theExpression = ""
        
        if forPanel == True:
            #generate a normalized nuke expression from which to read the curve values
            #when animating things in the panel
            
            c = "1"
            b = "0"
            
            try:
                w = str(max(float(self.wavelength.text()),1.0))
            except:
                w = "1"
            
            try:
                o = str(float(self.offset.text()))
            except:
                o = "0"

            try:
                cutoff = str(max(float(self.bcutoff.text()),0.6))
            except:
                cutoff = "0.95"

        else:
            #generate the final expression to put into nuke
            c = "(a_maxValue_%s - a_minValue_%s)" % (self.theKnobName,self.theKnobName)
            b = "a_minValue_%s" % (self.theKnobName)
            w = "a_wavelength_%s" % (self.theKnobName)
            o = "a_offset_%s" % (self.theKnobName)


        
        if theWaveType == "Sine":
            #(((sin(((frame*((pi * 2)/(w/2))/2) + o))+1)/2) * c ) + b
            theExpression = "((sin(((frame*((pi * 2)/(%s/2))/2) + %s))+1)/2)" %(w,o)
        
        
        elif theWaveType == "Random":
            #((random((frame/waveLength)+offset)) * (maxVal-minVal) ) + minVal
            theExpression = "(random((frame/%s)+%s))" %(w,o)

        elif theWaveType == "Noise":
            #(((1*(noise((frame/waveLength)+offset))+1 ) /2 ) * (maxVal-minVal) ) + minVal
            theExpression = "((1*(noise((frame/%s)+%s))+1 ) /2 )" %(w,o)

        elif theWaveType == "Triangle":
            #(((((2*asin(sin(2*pi*(frame/waveLength)+offset)))/pi) / 2)+0.5) * (maxVal-minVal) ) + minVal
            theExpression = "((((2*asin(sin(2*pi*(frame/%s)+%s)))/pi) / 2)+0.5)" %(w,o)

        elif theWaveType == "Sawtooth":
            #((1/waveLength)*(((frame-1)+offset) % waveLength) * (maxVal-minVal) ) + minVal
            theExpression = "(1/"+w+")*(((frame-1)+"+o+") % "+w+")"

        elif theWaveType == "Sawtooth Curved":
            #((sin((1/(pi/2))*(((frame-1)+offset)/(waveLength/2.46666666)) % (pi/2)))>0.99999? 1 : (sin((1/(pi/2))*(((frame-1)+offset)/(waveLength/2.46666666)) % (pi/2))) * (maxVal-minVal) ) + minVal
            theExpression = "(sin((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/2.46666666)) % (pi/2)))>0.99999? 1 : (sin((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/2.46666666)) % (pi/2)))"

        elif theWaveType == "Sawtooth Curved Rev.":
            #((cos((1/(pi/2))*(((frame-1)+offset)/(waveLength/2.46666666)) % (pi/2)))>0.99999? 1 : (cos((1/(pi/2))*(((frame-1)+offset)/(waveLength/2.46666666)) % (pi/2))) * (maxVal-minVal) ) + minVal
            theExpression = "(cos((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/2.46666666)) % (pi/2)))>0.99999? 1 : (cos((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/2.46666666)) % (pi/2)))"

        elif theWaveType == "Sawtooth Exponential":
            #((((((exp((1/(pi/2))*(((frame-1)+offset)/(waveLength/4.934802)) % pi*2)))/534.5)) - 0.00186741)>0.999987? 1 : (((((exp((1/(pi/2))*(((frame-1)+offset)/(waveLength/4.934802)) % pi*2)))/534.5)) - 0.00186741) * (maxVal-minVal) ) + minVal
            theExpression = "(((((exp((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/4.934802)) % pi*2)))/534.5)) - 0.00186741)>0.999987? 1 : (((((exp((1/(pi/2))*(((frame-1)+"+o+")/("+w+"/4.934802)) % pi*2)))/534.5)) - 0.00186741)"
        
        elif theWaveType == "Bounce":
            #((sin(((frame/waveLength)*pi)+offset)>0?sin(((frame/waveLength)*pi)+offset):cos((((frame/waveLength)*pi)+offset)+(pi/2))) * (maxVal-minVal) ) + minVal
            theExpression = "(sin(((frame/%s)*pi)+%s)>0?sin(((frame/%s)*pi)+%s):cos((((frame/%s)*pi)+%s)+(pi/2)))" %(w,o,w,o,w,o)


        #add the ease expression if there is one
        if easeExpression:
            theExpression = "(%s) * (%s)" %(theExpression,easeExpression)

        #then set max and min
        theExpression = "((%s) * %s) + %s" %(theExpression, c, b)


        #SQUARIFY
        if self.squarifyOld == True:
            if forPanel:
                c05 = "0.5"
                theMax = "1"
                theMin = "0"
            else:
                c05 = "(((a_maxValue_%s - a_minValue_%s)/2)+a_minValue_%s)" % (self.theKnobName,self.theKnobName,self.theKnobName)
                theMax = "a_maxValue_%s" % (self.theKnobName)
                theMin = "a_minValue_%s" % (self.theKnobName)
            
            
            theExpression = "(%s) > %s ? %s : %s" %(theExpression,c05,theMax,theMin)

        #BLIPPIFY
        if self.blipOld == True:
            if forPanel:
                theMax = "1"
                theMin = "0"
            else:
                theMax = "a_maxValue_%s" % (self.theKnobName)
                theMin = "a_minValue_%s" % (self.theKnobName)
                cutoff = "(a_bcutoff_%s * (%s - %s)) + %s" % (self.theKnobName,theMax,theMin,theMin)
                
                
            theExpression = "(%s) > %s ? %s : %s" %(theExpression,cutoff,theMax,theMin)


        return theExpression
            



    def getWaveEaseExpression(self,forPanel):

        easeExpression = self.getEaseExpression(forPanel)
        return self.getWaveExpression(forPanel,easeExpression)



def floatRange(start, stop, step):
    assert step > 0.0
    total = start
    compo = 0.0
    while total <= stop:
        yield total
        y = step - compo
        temp = total + y
        compo = (temp - total) - y
        total = temp
    

#################################
#        PARTICLE CLASS         #
#################################

class Particle():
    
    # Initialise
    
    def __init__(self, graphicsWindow, rad, pos):
        
        self.pos = pos
        self.radius = rad
        self.updateCount = 0
        
        
        #-------------------graphics----------------------
        #get reference to main window
        self.graphicsWindow = graphicsWindow
        
        #make small circle shape
        self.graphic = QtGui.QGraphicsEllipseItem(0,0,self.radius*2,self.radius*2)
        
        #no border
        pen = QtGui.QPen()
        pen.setStyle(QtCore.Qt.NoPen)
        self.graphic.setPen(pen)
        
        self.setParticleColour(100,200,100)
        
        #set transform origin to centre of ball
        self.graphic.setTransformOriginPoint(QtCore.QPointF(self.radius, self.radius))
        self.graphic.setAcceptsHoverEvents(False)
        self.graphic.setZValue(10) #always on top
        
        #add this to the scene
        self.graphicsWindow.scene.addItem(self.graphic)
    
    
    def move(self,newPos):
        
        #update position
        self.pos = newPos
        gPosX = self.pos[0] - self.radius
        gPosY = self.pos[1] - self.radius
        self.graphic.setPos( gPosX, gPosY )
    
    def scale(self,factor):
        
        #update scale factor
        self.graphic.setScale(factor)

    def fade(self,factor):
        
        self.setParticleColour(factor,factor,factor)
    
    def setParticleColour(self,r,g,b):
        
        #filled with chosen colour
        brush = QtGui.QBrush()
        brush.setColor( QtGui.QColor(r,g,b) )
        brush.setStyle( QtCore.Qt.SolidPattern )
        self.graphic.setBrush(brush)




class lineGraphic(QtGui.QGraphicsLineItem):
    
    def __init__(self, parent, x1,y1,x2,y2,colour):
        
        QtGui.QGraphicsLineItem.__init__(self,x1,y1,x2,y2)
        
        self.points = [[float(x1),float(y1)],[float(x2),float(y2)]]
        
        lineWidth = 2
        
        pen = QtGui.QPen()
        pen.setColor( colour )
        pen.setWidth(lineWidth)
        self.setPen(pen)

        blur = QtGui.QGraphicsBlurEffect(parent)
        blur.setBlurRadius(lineWidth*3)
        self.setGraphicsEffect(blur)



























