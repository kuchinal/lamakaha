KnobScripter v1.0 (Updated Jan 31 2017)

INFORMATION:

KnobScripter is a little nuke python tool to make it simpler to script on callback or python knobs.
It works as a floating panel to be called on a selected node, and as a dockable pane.
Once installed, KnobScripter can be opened on Edit/Node/Open Floating Knob Scripter (shortcut alt+z).

Tutorial video: https://vimeo.com/adrianpueyo/knobscripter


FIRST-TIME INSTALLATION INSTRUCTIONS:

1. Copy the included knob_scripter.py file inside of your ~/.nuke folder.
2. Inside your ~/.nuke folder, open menu.py with any text editor, or create it if it doesn't exist.
3. Add the following line to your menu.py:

import knob_scripter

4: Restart nuke, and you should now have knob_scripter installed.


UPDATE INSTRUCTIONS:

Just copy the knob_scripter.py folder from your new zip file to your ~/.nuke directory (replacing the old file).
The rest should now be set, restart Nuke and enjoy.


LICENSE:

Copyright (c) 2017, Adrian Pueyo
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Credit goes to Wouter Gilsing for the script editor widget part, which he made for his tool W_Hotbox.
It can be downloaded here: http://www.nukepedia.com/python/ui/w_hotbox



KnobScripter by Adrian Pueyo
adrianpueyo.com, 2017
