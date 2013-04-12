Download PyGame http://www.pygame.org/download.shtml

Compile with SDL-mixer support

Download the libtcod 1.5.1 archive from http://doryen.eptalys.net/libtcod/download/

For windows, libtcodpy.py, libtcod-mingw.dll and SDL.dll needs to be in the root directory. For other platforms, copy in the equivalent files. (libtcodpy.py is possibly the same across all platforms)


EDITOR
python editor.py <mapname> <width> <height>
...to edit a new or existing map called <mapname>.
Specifying a widht and height has no meaning if we are loading a pre-existing map.

To save: close the editor by hitting ESC. Closing the editor by clicking the 'x' will not save the map. Yes, this is retarded (and therefore subject to change).

Controls:
Click the palette in the right side panel to pick a brush
Hold space and move the mouse to pan the map. Libtcod's mouse movement values appear to be a bit wonky, so small mouse movements tend not to register. (this might get fixed by switching to a newer version of libtcod)

Mouse wheel - change brush size
b - toggle brush shape between round and square


LIGHT TEST
python lighttest.py

This is a visual test to see what lighting would look like. Left in the window to create new point lights. Right-click to remove point-lights. Will crash if you attempt to remove the last light.
Pretty primitive - doesn't check for index out-of-bounds at the moment. 

c - recalculate the light map
