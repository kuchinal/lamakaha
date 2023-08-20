"""
backdropTools.py: A set of functions to easily control
the layout and color of Nuke backdrops

Ivan Busquets - 2011
"""

import nuke, nukescripts
import random

###############################################################
# COLOR CONVERSIONS
#
#       RGBtoHSL
#       HSLtoRGB
#       TILEtoHSL
#       HSLtoTILE
#       TILEtoRGB
#       RGBtoTILE
#       TILEtoHSV
#       HSVtoTILE
#       HSVtoRGB
#       RGBtoHSV
###############################################################
def RGBtoHSL(R, G, B):
    '''
    RGBtoHSL(R, G, B) -> tuple
    
    Returns a tuple representing Hue, Saturation, and Luminance values
    in a 0-1 range.
    
    Keyword arguments:
    R, G, B -- float values for Red, Green and Blue, in the 0-1 range
    '''
    maxRGB = max(R, G, B)
    minRGB = min(R, G, B)
    H = S = L = (maxRGB + minRGB) / 2.0
    
    if maxRGB == minRGB:
        H = S = 0.0  # no saturation, Hue is undefined
    else:
        delta = maxRGB - minRGB
        if L > 0.5:
            S = delta / float(2 - maxRGB - minRGB)
        else:
            S = delta / float(maxRGB + minRGB)
        
        if maxRGB == R:
            H = (G - B) / float(delta)
            if G < B:
                H += 6
                
        elif maxRGB == G:
            H = (B - R) / float(delta) + 2
            
        else:
            H = (R - G) / float(delta) + 4
            
        H /= 6.0
        
    return H, S, L


def HSLtoRGB(H, S, L):
    '''
    HSLtoRGB(R, G, B) -> tuple
    
    Returns a tuple of Red, Green, and Blue values in the 0-1 range
    from Hue, Saturation, and Luminance values.
    
    Keyword arguments:
    H, S, L -- float values for Hue, Saturation and Luminance,
    in the 0-1 range
    '''
    R = G = B = L
    
    if S == 0.0:
        return R,G,B
    else:
        def hue2rgb(p,q,t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6.0: return p + (q - p) * 6.0 * t
            if t < 1/2.0: return q
            if t < 2/3.0: return p + (q - p) * (2/3.0 - t) * 6.0
            return p 
 
        q = L * (1 + S) if L < 0.5 else L + S - L * S
        p = 2 * L - q
        R = hue2rgb(p, q, H + 1/3.0)
        G = hue2rgb(p, q, H)
        B = hue2rgb(p, q, H - 1/3.0)
    return R,G,B

def TILEtoHSL(V):
    '''
    TILEtoHSL(V) -> tuple
    
    Returns a tuple representing Hue, Saturation, and Luminance values
    in a 0-1 range, from a 32 bit int as returned by the "tile_color" knob.
    
    Keyword arguments:
    V -- a 32 bit int as returned by the "tile_color" knob
    '''
    return RGBtoHSL(*TILEtoRGB(V))

def HSLtoTILE(H, S, L):
    '''
    HSLtoTILE(H, S, L) -> int
    
    Returns a 32 bit int ready to feed into a "tile_color" knob, from
    Hue, Saturation and Luminance values in the 0-1 range.
    
    Keyword arguments:
    H,S,L -- float values for Hue, Saturation and Luminance,
    in the 0-1 range
    '''
    R,G,B = HSLtoRGB(H,S,L)
    return int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 )

def TILEtoRGB(V):
    '''
    TILEtoRGB(V) -> tuple
    
    Returns a tuple representing Red, Green, and Blue values
    in a 0-1 range, from a 32 bit int as returned by the "tile_color" knob.
    
    Keyword arguments:
    V -- a 32 bit int as returned by the "tile_color" knob
    '''

    R = (0xFF & V >> 24) / 255.0
    G = (0xFF & V >> 16) / 255.0
    B = (0xFF & V >> 8) / 255.0
    return R,G,B

def RGBtoTILE(R,G,B):
    '''
    RGBtoTILE(R, G, B) -> int
    
    Returns a 32 bit int ready to feed into a "tile_color" knob, from
    Red, Green and Blue values in the 0-1 range.
    
    Keyword arguments:
    R,G,B -- float values for Hue, Saturation and Value, in the 0-1 range
    '''
    return int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 )

def TILEtoHSV(V):
    '''
    TILEtoHSV(V) -> tuple
    
    Returns a tuple representing Hue, Saturation, and Value values
    in a 0-1 range, from a 32 bit int as returned by the "tile_color" knob.
    
    Keyword arguments:
    V -- a 32 bit int as returned by the "tile_color" knob
    '''   
    return RGBtoHSV(*TILEtoRGB(V))

def HSVtoTILE(H, S, V):
    '''
    HSLtoTILE(H, S, V) -> int
    
    Returns a 32 bit int ready to feed into a "tile_color" knob, from
    Hue, Saturation and Value values in the 0-1 range.
    
    Keyword arguments:
    H,S,V -- float values for Hue, Saturation and Value, in the 0-1 range
    '''
    
    R,G,B = HSVtoRGB(H,S,V)
    return int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 )

def HSVtoRGB(H,S,V):
    '''
    HSVtoRGB(R, G, B) -> tuple
    
    Returns a tuple of Red, Green, and Blue values in the 0-1 range
    from Hue, Saturation, and Value values.
    
    Keyword arguments:
    H, S, V -- float values for Hue, Saturation and Value, in the 0-1 range
    '''

    i = math.floor(H * 6.0)
    f = H * 6.0 - i
    p = V * (1 - S)
    q = V * (1 - f * S)
    t = V * (1 - (1 - f) * S)

    if (i % 6) == 0:
        R = V
        G = t
        B = p
    elif (i % 6) == 1:
        R = q
        G = V
        B = p
    elif (i % 6) == 2:
        R = p
        G = V
        B = t
    elif (i % 6) == 3:
        R = p
        G = q
        B = V
    elif (i % 6) == 4:
        R = t
        G = p
        B = V
    elif (i % 6) == 5:
        R = V
        G = p
        B = q

    return R , G , B
    

def RGBtoHSV(R, G, B):
    '''
    RGBtoHSV(R, G, B) -> tuple
    
    Returns a tuple representing Hue, Saturation, and Value values
    in a 0-1 range.
    
    Keyword arguments:
    R, G, B -- float values for Red, Green and Blue, in the 0-1 range
    '''
    #Clamp rgb values
    R = min(max(0,R),1)
    G = min(max(0,G),1)
    B = min(max(0,B),1)

    H = S = 0.0
    V = max( R, G, B )
    
    minRGB = min( R, G, B )

    delta = V - minRGB

    S = 0
    H = 0

    if V != 0:
        S = delta / float(V)
    else: # saturation is then 0, and hue is undefined
        return H,S,V

    if S == 0.0:
        return H,S,V

    if V == R:
        H = ( G - B ) / float(delta) 
    elif V == G:
        H = 2 + ( B - R ) / float(delta)
    else:
        H = 4 + ( R - G ) / float(delta)

    H *= 60.0/360.0
    if H >= 1.0:
        H-= 1.0
    if H < 0.0:
        H+= 1.0

    return H,S,V

###############################################################
# BACKDROP REORDERING
#
#       selectBackdropContents
#       nodeInBackdrop
#       nodesInBackdrop
#       fixBackdropDepth
###############################################################

def selectBackdropContents(backdropNode):
    '''Select all nodes inside a backdrop.
    There is a built in method for this on Nuke6.3v5,
    but this is kept here to expand compatibility
    to earlier versions
    '''
    bx, by = backdropNode.xpos(), backdropNode.ypos()
    nukescripts.clear_selection_recursive()
    backdropNode.setSelected(True)
    nuke.nodeCopy(nukescripts.cut_paste_file())
    nuke.nodeDelete(popupOnError=False)
    nuke.nodePaste(nukescripts.cut_paste_file())
    nuke.selectedNode().setXYpos(bx, by)

   
def nodeInBackdrop(node, backdropNode):
    '''
    nodeInBackdrop(node, backdropNode) -> bool
    
    Returns whether the passed-in node is fully contained within the backdrop
    '''

def nodesInBackdrop(backdropNode):
    '''
    nodesInBackdrop(backdropNode) -> bool
    
    Returns all nodes contained within the backdrop
    '''
    return [n for n in nuke.allNodes() if nodeInBackdrop(n,backdropNode)]
    
def fixBackdropDepth():
    '''
    Layer smaller backdrops on top of bigger ones
    '''
    sel = nuke.selectedNodes('BackdropNode')
    all = nuke.allNodes('BackdropNode')
    all.sort(key = lambda x: x.screenHeight() * x.screenWidth(), reverse = True)
    try:
        [b.selectNodes() for b in all if (b in sel or len(sel) ==0)]
    except: # This will be used for Nuke versions below 6.3v5
        [selectBackdropContents(b) for b in all if (b in sel or len(sel) ==0)]
        
def fixBackdropDepthMy():      
    n = nuke.selectedNode()
    p = n['z_order'].setValue(-1)
    
###############################################################
# BACKDROP SHIFTING
#
#       shiftBackdropHue
#       shiftBackdropHue2 (alternative method, uses HSV instead of HSL)
#       shiftBackdropLuma
#       shiftBackdropSat
#       spreadBackdropHues
###############################################################

def shiftBackdropHue(step = 0.1):
    '''
    Change the hue of the currently selected backdrop node(s).
    
    Keyword arguments:
    step -- amount by which to increase/decrease the current hue value,
            in the 0-1 range. (1 = 360 degrees)
    '''
    backdrops = nuke.selectedNodes('BackdropNode')
    for bd in backdrops:
        current = bd['tile_color'].value()
        h,s,l = TILEtoHSL(current)
        h += step
        bd['tile_color'].setValue(HSLtoTILE(h,s,l))
        
def shiftBackdropHue2(step = 0.1):
    '''
    Alternative method to change the hue of the currently selected backdrop
    node(s), preserving the maximum Value instead of Luminance.
    
    Keyword arguments:
    step -- amount by which to increase/decrease the current hue value,
            in the 0-1 range. (1 = 360 degrees)
    '''
    backdrops = nuke.selectedNodes('BackdropNode')
    for bd in backdrops:
        current = bd['tile_color'].value()
        h,s,v = TILEtoHSV(current)
        h += step
        bd['tile_color'].setValue(HSVtoTILE(h,s,v))
        
def shiftBackdropLuma(step = 0.1, wrap = False):
    '''Change the luminance of the currently selected backdrop node(s)

    Keyword arguments:
    step -- amount by which to increase/decrease the current Luminance
    wrap -- whether values should be clamped, or wrapped around when pushed beyond 0 and 1
    '''
    backdrops = nuke.selectedNodes('BackdropNode')
    for bd in backdrops:
        current = bd['tile_color'].value()
        h,s,l = TILEtoHSL(current)
        l += step
        if wrap and l>1:
            l -= 1
        if wrap and l<0:
            l += 1
        # Avoid going fully desaturated by going luma == 0 or luma == 1
        l = max(0.01, min(l, 0.99))
        bd['tile_color'].setValue(HSLtoTILE(h,s,l))

def shiftBackdropSat(step = 0.1, wrap = False):
    '''Change the hue of the currently selected backdrop node(s)

    Keyword arguments:
    step -- amount by which to increase/decrease the current Saturation
    wrap -- whether values should be clamped, or wrapped around when pushed beyond 0 and 1
    '''
    backdrops = nuke.selectedNodes('BackdropNode')
    for bd in backdrops:
        current = bd['tile_color'].value()
        h,s,l = TILEtoHSL(current)
        s += step
        if wrap and s>1:
            s -= 1
        if wrap and s<0:
            s += 1
        # Avoid going fully desaturated by going s == 0 or s == 1
        s = max(0.01, min(s, 0.99))
        bd['tile_color'].setValue(HSLtoTILE(h,s,l)) 

def spreadBackdropHues(randomize = True):
    '''
    Evenly spread the hue of the currently selected backdrop node(s).
    Guarantees maximum color separation between the selected backdrops.

    Keyword arguments:
    randomize -- If True, randomizes the order in which to color
                 the selected backdrops, so that running this multiple
                 times will produce different results.
    '''
    backdrops = nuke.selectedNodes('BackdropNode')
    if not backdrops:
        return
    step = 1 / float(len(backdrops))
    k = 0
    
    if randomize:
        random.shuffle(backdrops)
        k += random.random()
        
    for idx, bd in enumerate(backdrops):
        current = bd['tile_color'].value()
        h,s,l = TILEtoHSL(current)
        if s == 0:  # If tile has 0 saturation, bring saturation up so we can change the color
            s = 0.5
                        
        h = idx*step + k
        
        if h > 1:
            h -= 1
        if h < 0:
            h += 1
        
        bd['tile_color'].setValue(HSLtoTILE(h,s,l))


###############################################################################
# Example implementation into Nuke menus

def addStandardShortcuts():
    '''
    Call this from menu.py to set up the default menu items and keyboard shortcuts
    '''
    m = nuke.menu('Nuke')
    m.addCommand("Edit/Backdrops/Fix Layering", "backdropTools.fixBackdropDepth()")
    m.addCommand("Edit/Backdrops/Shift Hue", "backdropTools.shiftBackdropHue()")
    m.addCommand("Edit/Backdrops/Spread Hues", "backdropTools.spreadBackdropHues()")
    m.addCommand("Edit/Backdrops/Luma +", "backdropTools.shiftBackdropLuma(step = 0.1)")
    m.addCommand("Edit/Backdrops/Luma -", "backdropTools.shiftBackdropLuma(step = -0.1)")
    m.addCommand("Edit/Backdrops/Sat +", "backdropTools.shiftBackdropSat(step = 0.1)")
    m.addCommand("Edit/Backdrops/Sat -", "backdropTools.shiftBackdropSat(step = -0.1)")
