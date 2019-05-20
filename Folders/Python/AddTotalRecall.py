def AddTotalRecall():
    import nuke

    setcount = 6
    n = nuke.selectedNode()
    badlist = ['channel', 'channels', 'maskChannelInput', 'unpremult', 'layer', 'maskChannel', 'maskChannelMask', 'Mask', 'mask', 'lookup', 'format']


        
    t = nuke.Tab_Knob('store_Sets', 'Sets')
    n.addKnob(t)

    button = 0

    for i in range(1,setcount):   
        b_set = """badlist = """ + str(badlist) + """
n = nuke.thisNode()
ak = n.knobs()
li = []
for raus in ak:
    if "store" in raus:
        li.append(raus)
for raus in li:
    del ak[raus]
for badknob in badlist:
    try:
        del ak[badknob]
    except:
        pass
storeme= {}
for b in ak:
    storeme[b] = ak[b].getValue()

storeHere = 'store_'+str(""" + str(i) + """)        
n[storeHere].setValue(str(storeme))"""
        tk = nuke.PyScript_Knob('store_b_set'+str(i), 'Set '+str(i))
        tk.setValue(b_set)
        n.addKnob(tk)


    line = nuke.Text_Knob('store_bla', '')
    n.addKnob(line)

    for i in range(1,setcount):  
        b_recall="""import ast
n = nuke.thisNode()
readHere = 'store_'+str(""" + str(i) + """) 
readme = ast.literal_eval(n[readHere].getValue())
print readme
for knob in readme:
    setme = readme[knob]
    print knob
    try:
        n[knob].setValue(setme) 
    except TypeError:
        try:
            n[knob].setValue(str(setme))
        except TypeError:    
            n[knob].setValue(bool(setme))"""

        tk = nuke.PyScript_Knob('store_b_recall'+str(i), 'Recall '+str(i))
        tk.setValue(b_recall)
        n.addKnob(tk)


    for i in range(1,setcount):  

        tk = nuke.String_Knob('store_'+str(i), '')
        tk.setFlag(nuke.INVISIBLE)
        n.addKnob(tk) 


            
