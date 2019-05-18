a = nuke.selectedNode()['add'].value()
print a
if a is float:
    print "float"
elif a is str:
    print "string"

if isinstance(a, basestring):
    print "string"

if isinstance(a, float):
    print "float"

if nuke.selectedNode()['add'].isAnimated():
    print "expression"


#some additional expression check:

    index = 0
if knob.hasExpression(index):
origExpression = knob.animation(index).expression()
newExpression = "(%s)/2" % origExpression
knob.setExpression(newExpression, index)

http://community.thefoundry.co.uk/discussion/topic.aspx?f=190&t=102170