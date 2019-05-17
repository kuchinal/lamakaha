

import nuke
def knobDefaults():
	nuke.knobDefault( 'DirBlurWrapper.channels', 'rgba' )
	nuke.knobDefault( 'DirBlurWrapper.BlurType', 'linear' )
	nuke.knobDefault( 'Read.on_error', 'checkerboard' )
	nuke.knobDefault( 'DeepRead.on_error', 'checkerboard' )
	nuke.knobDefault( 'DeepRead.black_outside', "1" )
	nuke.knobDefault( 'Wireframe.operation', 'see through' )