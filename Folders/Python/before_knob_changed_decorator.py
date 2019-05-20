# ss_before_knob_changed by Daniel Flehner Heen @ www.stormstudios.no
#
# Decorator function to increase speed of nodes with "heavy" custom callbacks.
# Speeds up the overall performance of nuke when using customized nodes
#
#
# Usage:
#
#    import time  # Only for this example
#    from before_knob_changed_decorator import ss_before_knob_changed


#    # Sluggish moronic callback
#    # Try it with and without the decorator to see the difference
#    @ss_before_knob_changed
#    def my_callback():
        #time.sleep(0.2)

#    # Get node to apply callback to
#    node = nuke.selectedNode()

#    # Apply custom callback.
#    node.knob('knobChanged').setValue('my_callback()')


import nuke

from functools import wraps


def ss_before_knob_changed(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        knob = nuke.thisKnob()
        if knob is not None:
            if knob.name() in ['xpos', 'ypos', 'selected']:
                return

        return callback(*args, **kwargs)

    return wrapper
