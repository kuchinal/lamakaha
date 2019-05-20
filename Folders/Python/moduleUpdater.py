# Set this to the OS environment variable of your home directory (somewhere you have write access)
# !! ESSENTIAL !! - If moduleUpdater doesn't work properly, check whether this is correct.
homedir = "//INFERNO2/projects/infinite/home/aku/user/Python/"

# Shows modules loaded in Nuke and lets you easily update/execute them for when you are modifying them.
# Even works with panels, just follow the instructions of the tool.

# v1.3
# ....
# Replace "Src to Clipboard" with "Open .py-File"
#
# v1.2
# 08/10/2012
# Selected module is restored after layout restoration
# Added a text field to input which layout to restore instead of prompting each time
#
# v1.1 
# 28/09/2012 
# Added messages boxes to react to various errors
# (updating modules with empty "Path to Scripts"-field, deleting a py-File and then selecting that module)
#
# v1.0
# 27/09/2012 Andreas Opferkuch
#
# Based on callExternalUpdatedFunction (http://www.nukepedia.com/python/misc/call-updated-function/):
# 06/2010 Andreas Frickinger

"""
attempts to extract function lists of modules. kept for future reference. stream redirection and python doc generation may come in handy.

---------- ATTEMPT 1 -----------
# initial thought: help() on module, redirect stdout to capture list after "FUNCTIONS"
from cStringIO import StringIO

oldstdout = sys.stdout
sys.stdout = mystdout = StringIO()

help(module)

sys.stdout = oldstdout
str = mystdout.getvalue()

---------- ATTEMPT 2 -----------
import pydocs

# read docs for selected module
strHelp = pydoc.plain(pydoc.render_doc(module))

# get names of functions - if available
lstFunctions = []
if "FUNCTIONS" in strHelp: # and (not "panel" in strHelp.lower()):
  lstHelp = strHelp.rpartition("FUNCTIONS")[2].partition("DATA")[0].split("\n")

  # parse function names
  for strHelp in lstHelp:
    strFunction = strHelp.strip().partition("(")[0]
    if strFunction != "":
      lstFunctions.append(strFunction)
      
  self.functionList.setValues(lstFunctions)
  
  # if only one function in list, set that as current one
  if len(lstFunctions) == 1:
    self.function.setValue(lstFunctions[0])
else:
  self.functionList.setValues(lstFunctions)
  self.function.setValue("No executable function found")

"""

import inspect
import subprocess
from PySide import QtGui # needed for clipboard access

import nuke
import nukescripts
import sys
import os

import time

package = ""
module = ""
function = ""

def moduleUpdate(module, function, package = "", ispanel = False):
    if package != "":
      package += "."
    
    exec("import " + package + module + " as importedModule")
    reload(importedModule)
    
    if not ispanel:
      exec("importedModule." + function + "()")
        
class moduleUpdater(nukescripts.PythonPanel):
  def saveSettings(self):
    # save path to ini-file
    iniFile = open(os.environ.get(homedir) + "moduleUpdater.ini", "w")
    settings = self.path.value() + "," + self.package.value() + "," + self.moduleList.value() + "," + self.module.value() + "," + self.functionList.value() + "," + self.function.value() + "," + str(self.restoreLayout.value())
    iniFile.write(settings)
    iniFile.close()

  def updateModuleList(self):
    path = self.path.value()
    if self.path.value() == "":
      self.moduleList.setValues([])
      self.module.setValue("")
      self.functionList.setValues([])
      self.function.setValue("")
      return
      
    allmodules = sys.modules
    iter = allmodules.itervalues()
    
    modules = []
    
    while True:
      try:
        strCurrModule = str(iter.next())
        if path in strCurrModule:
          strCurrModule = strCurrModule[9:strCurrModule.find("'", 9)]
          modules.append(strCurrModule)
          #print strCurrModule
      except:
          break
          
    modules.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
    self.moduleList.setValues(modules)
    self.moduleList.setValue(1)

  def __init__( self ):
    nukescripts.PythonPanel.__init__( self, "Module Updater", "uk.co.thefoundry.moduleUpdater")
    self.package = nuke.String_Knob("package", "Package (optional):" )
    self.addKnob(self.package)
    
    self.restoreLayout = nuke.Int_Knob("restoreLayout", "Curr. window layout:" )
    self.restoreLayout.setTooltip("This is used if you update a panel. The window layout has to be restored in order for panels to be updated.")
    self.restoreLayout.clearFlag(nuke.STARTLINE)
    self.addKnob(self.restoreLayout)
    
    self.moduleList = nuke.Enumeration_Knob("moduleList", "Module List:", [""])
    self.addKnob(self.moduleList)
    
    self.module = nuke.String_Knob("module", "Module:" )
    self.addKnob(self.module)

    self.functionList = nuke.Enumeration_Knob("functionList", "Function List:", [""])
    self.addKnob(self.functionList)
    
    self.function = nuke.String_Knob("function", "Function:" )
    self.addKnob(self.function)
    
    self.cmdGo = nuke.PyScript_Knob("cmdGo", "Refresh && Execute")
    self.cmdGo.setFlag(nuke.STARTLINE)
    self.addKnob(self.cmdGo)

    self.cmdPrint = nuke.PyScript_Knob("cmdPrint", "Print Source")
    self.addKnob(self.cmdPrint)

    self.cmdClipboard = nuke.PyScript_Knob("cmdClipboard", "Open .py-File")
    self.addKnob(self.cmdClipboard)
    
    self.path = nuke.String_Knob("path", "Path to Scripts:")
    self.path.setTooltip("Just the drive (e.g. H:) is sufficient for filtering, unless you want something more specific.")
    self.addKnob(self.path)
    
    self.cmdUpdate = nuke.PyScript_Knob("cmdUpdate", "Update Modules")
    self.addKnob(self.cmdUpdate)
    
    self.defaultSettings = []
    # get path to scripts, set to home directory by default
    try:
      iniFile = open(os.environ.get(homedir) + "moduleUpdater.ini", "r")
      self.defaultSettings = (iniFile.read()).split(",")
      defaultUpdatePath = defaultSettings[0]
      iniFile.close()
    except:
      defaultUpdatePath = (os.environ.get(homedir))[0:2]
      iniFile = open(os.environ.get(homedir) + "moduleUpdater.ini", "w")
      iniFile.write(defaultUpdatePath)
      iniFile.close()
      
    self.path.setValue(defaultUpdatePath)
    
    # create lists if default path is set - which i really should be at this point (either through ini or default path)
    if defaultUpdatePath != "":
      self.updateModuleList()

    # default window layout value
    self.restoreLayout.setValue(3)
    
    # if ini file existed in which defaultmodule was saved, restore all stored values
    try:
      defaultModule = self.defaultSettings[3]
      if defaultModule != "":
        self.package.setValue(self.defaultSettings[1])
        self.moduleList.setValue(self.defaultSettings[2])
        self.module.setValue(defaultModule)
        self.knobChanged(self.moduleList)
        self.functionList.setValue(self.defaultSettings[4])
        self.function.setValue(self.defaultSettings[5])
        self.restoreLayout.setValue(int(self.defaultSettings[6]))
      else:
        self.knobChanged(self.moduleList)
    except:
      return

  def knobChanged(self, knob):
    # refresh & execute
    if knob == self.cmdGo:
      global package
      global module
      global function
      package = self.package.value()
      module = self.module.value()
      function = self.function.value()

      if function == "Panel? (Leave this if it is)":
        #userInput = nuke.getInput('For a panel refresh, the whole window layout has to be updated.\nEnter the number of the window layout you want to restore', '1')
        #layoutToRestore = int(userInput)
        layoutToRestore = self.restoreLayout.value()
        if layoutToRestore > 0:
          moduleUpdate(module, function, package, True)
          #nuke.getPaneFor("uk.co.thefoundry.moduleUpdater").destroy()
          nuke.restoreWindowLayout(layoutToRestore)
      else:
        moduleUpdate(module, function, package)
      
    # print source of module
    elif knob == self.cmdPrint:
      try:
        print inspect.getsource(sys.modules.get(self.module.value()))
      except:
        nuke.message("Sorry, didn't work")
        
    # copy source of module to clipboard
    elif knob == self.cmdClipboard:
      allmodules = sys.modules
      iter = allmodules.itervalues()
      
      while True:
        try:
          strCurrModule = str(iter.next())
          if module in strCurrModule:
            pyfile = strCurrModule.replace("\\","\\\\").replace("/","\\\\")
            pyfile = pyfile[pyfile.find("from")+6:(pyfile.find(".py")+3)]
            try:
              subprocess.Popen('cmd /c start ' + pyfile)
              #srcModule = inspect.getsource(sys.modules.get(self.module.value()))
              #clipboard = QtGui.QApplication.clipboard()
              #clipboard.setText(srcModule) # set clipboard 
              break
            except:
              nuke.message("Sorry, didn't work")
            #print strCurrModule
        except:
            break
    
    # update list of modules
    elif knob == self.cmdUpdate:
      if self.path.value() == "":
        nuke.message("Module/function list require a path to work. You can still enter the name of your module with the function to execute manually though.")
        self.moduleList.setValues([])
        self.module.setValue("")
        self.functionList.setValues([])
        self.function.setValue("")
        return
      
      # update module list AND call callback for it to refresh function list as well
      self.updateModuleList()
      self.knobChanged(self.moduleList)
      
    # transfer selected function to text field
    elif knob == self.functionList:
      self.function.setValue(self.functionList.value())
    
    # transfer selected module to text field (and update function list)
    elif knob == self.moduleList:
      module = self.moduleList.value()
      if module != "":
        self.module.setValue(module)
        
        # reset current function name
        self.function.setValue("")
        
        # get function list for currently selected module
        strFunctions = []
        functions = inspect.getmembers(sys.modules.get(module), inspect.isfunction)
        for function in functions:
          strFunctions.append(function[0])
          
        self.functionList.setValues(strFunctions)
        
        # attempt to find out whether module is a panel
        try:
          moduleSource = inspect.getsource(sys.modules.get(module))
        except:
          nuke.message("Could not read the module. Please check whether the python file still exists or restart Nuke (Module Updater always shows the currently loaded modules).")
          return
          
        if "PythonPanel" in moduleSource or "QWidget" in moduleSource:
          self.function.setValue("Panel? (Leave this if it is)")
        elif len(strFunctions) == 1:
          self.function.setValue(strFunctions[0])
        elif strFunctions == []:
          self.function.setValue("No executable function found")
        
        # reset currently selected function list item to first one
        self.functionList.setValue(0)
        
    self.saveSettings()
        
def createModuleUpdater():
  return moduleUpdater().addToPane()
  
menu = nuke.menu("Pane")
menu.addCommand("Module Updater", createModuleUpdater)
nukescripts.registerPanel("uk.co.thefoundry.moduleUpdater", createModuleUpdater)
