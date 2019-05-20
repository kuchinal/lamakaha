def smMerge(nodeType):
    import nuke
    a = nuke.selectedNodes()
    al = []
    for node in a:
        al.append(node['xpos'].value())
        al.sort()
        al.reverse()


    amm =  len(al)
    new = [None]*amm
    p = 0
    while p< amm:   
        a = nuke.selectedNodes()
        for one in a:
            pos = one['xpos'].value()
            if pos == al[p]:
                new.insert(p,one)
        print new[:amm]
        p+=1

    q=1
    for node in new[:amm]: 
        if q==1:
            followed = node
            q+=1
        else:
            if nodeType== "MergeGeo":
                follower = nuke.nodes.MergeGeo()
            if nodeType== "MergeMat":
                follower = nuke.nodes.MergeMat()
            if nodeType== "DeepMerge":
                follower = nuke.nodes.DeepMerge()
            if nodeType== "Merge2":
                follower = nuke.nodes.Merge2()


            follower.setInput(0,followed)
            follower.setInput(1,node)
            followed = follower


def mergeThis():
    import nuke 
    try: 
        if 'shadow_override' in nuke.selectedNode().knobs() or 'Camera' in nuke.selectedNode().Class() or 'render_mode' in nuke.selectedNode().knobs() or 'Light' in nuke.selectedNode().Class() or 'DisplaceGeo' in nuke.selectedNode().Class() or 'Axis' in nuke.selectedNode().Class():
            if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeGeo")
            else:
                smMerge("MergeGeo")

        elif 'MergeMat' in nuke.selectedNode().Class() or 'project_on' in nuke.selectedNode().knobs() or 'Mat' in nuke.selectedNode()['name'].value(): 
             if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeMat")
             else:
                smMerge("MergeMat")
        elif "deep" in str(nuke.selectedNode().metadata()) and "depth" not in str(nuke.selectedNode().channels()) or "DeepRecolor" in nuke.selectedNode()['name'].value(): 
             if len(nuke.selectedNodes())==1:
                return nuke.createNode( "DeepMerge")
             else:
                smMerge("DeepMerge")
        else: 
            raise ValueError 
    except: 
         if len(nuke.selectedNodes())<=1:
            return nuke.createNode( "Merge2")

         else:
            smMerge("Merge2")

