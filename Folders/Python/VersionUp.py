import nuke
def VersionUp():	

	def Uptate(a,b):
	  n = nuke.selectedNodes()
	  for n in n:
	      z = n['file'].value()
	      t = z.replace(a,b)
	      z = n['file'].setValue(t)

	panel=nuke.Panel("Version Update")
	Old = panel.addSingleLineInput("Old Version","v000")
	New = panel.addSingleLineInput("New Version","v000")
	panel.show()

	a= panel.value('Old Version')
	b= panel.value('New Version')
	Uptate(a,b)
