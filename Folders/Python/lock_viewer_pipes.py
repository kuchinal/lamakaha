# author: Frank Rueter
# v1.1

import nuke

def __create_knobs(viewer_node):
    # lock knobs dosn't exist, create one and use default action
    tab = nuke.Tab_Knob('Lock')
    lock_all = nuke.Boolean_Knob('lock_all_buffers', 'lock all buffers')
    viewer_node.addKnob(tab)
    viewer_node.addKnob(lock_all)
    for i in xrange(1,10):
        k = nuke.Boolean_Knob('lock_buffer_{}'.format(i), 'lock buffer {}'.format(i))
        k.setFlag(nuke.STARTLINE)
        viewer_node.addKnob(k) 
    k = nuke.Boolean_Knob('lock_buffer_0', 'lock buffer 0') 
    k.setFlag(nuke.STARTLINE)
    viewer_node.addKnob(k)         


def connect_selected_to_unlocked_viewer(i):
    if i == 0:
        item = nuke.menu('Nuke').findItem('Viewer/Connect to A Side/Using Input 10')
    else:
        item = nuke.menu('Nuke').findItem('Viewer/Connect to A Side/Using Input {}'.format(i))
    
    # get the node
    try:
        vn = nuke.activeViewer().node()
    except AttributeError:
        # no viewer exists, use default behaviour which creaetes one
        item.invoke()
        vn = nuke.activeViewer().node()
    # check buffers then call the default action
    try:
        buffer_lock = vn['lock_buffer_{}'.format(i)].value()
        if not nuke.selectedNodes() or nuke.selectedNode().Class() == 'Viewer':
            # no nodes are selected or only a viewer node is selected - use default behaviour
            item.invoke()
        elif (vn['lock_all_buffers'].value() or buffer_lock):
            # viewer is locked
            if not buffer_lock:
                message = '{} is locked.'.format(vn.name())
            else:
                message = 'Buffer {} in {} is locked.'.format(i, vn.name())
            nuke.message(message)
        else:
            # viewer is unlocked
            item.invoke()
    except NameError:
        __create_knobs(vn)
        item.invoke()

def lock_buffers(_buffer, value):
    v = nuke.activeViewer()
    if _buffer == "current":
        # lock current buffer
        cur_buffer = v.activeInput() + 1
        cur_buffer = cur_buffer if cur_buffer != 10 else 0
        v.node()['lock_buffer_{}'.format(cur_buffer)].setValue(value)
    elif _buffer == "all":
        # lock all buffers
        v.node()['lock_all_buffers'].setValue(value)

def register_viewer_locks():
    # menu entries
    dagContext = 2
    m = nuke.menu('Nuke')
    hm = m.addMenu('hiddenMenu')
    hm.setVisible(False)
    for i in xrange(10):
        if i == 0:
            hm.addCommand("Using Input 10", "lock_viewer_pipes.connect_selected_to_unlocked_viewer(0)", "0", shortcutContext=dagContext)
        else:
            hm.addCommand("Using Input {}".format(i), "lock_viewer_pipes.connect_selected_to_unlocked_viewer({})".format(i), str(i), shortcutContext=dagContext)
    nuke.menu('Viewer').addCommand("lock/current buffer", "lock_viewer_pipes.lock_buffers('current', True)")
    nuke.menu('Viewer').addCommand("lock/all buffers", "lock_viewer_pipes.lock_buffers('all', True)")
    nuke.menu('Viewer').addCommand("unlock/current buffer", "lock_viewer_pipes.lock_buffers('current', False)")
    nuke.menu('Viewer').addCommand("unlock/all buffers", "lock_viewer_pipes.lock_buffers('all', False)")

        
