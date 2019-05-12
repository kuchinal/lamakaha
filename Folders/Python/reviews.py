import nuke
def reviews():
    new = nuke.toNode("Review")
    if new:
        nuke.show(new)
    else:
        nuke.nodePaste(UserDir+'Folders/NukeScripts/review.nk')
        new = nuke.toNode("Review")
        nuke.show(new)