import nuke
def PSolverLocators():
    panel = nuke.message("Please be sure you selected all Axises you want to copy \n Please be sure your ProjectionSolver node called ProjectionSolver1 \n After code will be evaluated hit Add Locator Button so you will see all locators")
    n = nuke.selectedNodes()
    number = 0
    for a in n:
     number = str(number)
     point = "p"+ number
     if a.Class()=="Axis":
      pos = a['translate'].value()
     pr = nuke.selectedNodes()
     PS=nuke.toNode("ProjectionSolver1")
     PS[point].setValue(pos)
     number = int(number)
     number = number + 1 


                                      
