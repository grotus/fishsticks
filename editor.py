import sys
from core.Light import AmbientLight
from core.Scene import Scene
from core.Tile import Tile
import tiles.SimpleTiles
import tiles.Nullspace
import libtcodpy as libtcod
from core import EngineSettings, Renderer, Core
from gui.BasePanel import BasePanel
from gui.LogPanel import LogPanel
from helpers.Helpers import *
from gui.Editor import PalettePanel, EditorMapWindow, Brush


if __name__ == '__main__':
    sys.argv.pop()
    for arg in sys.argv:
        print arg


#-----------------------------------------------------------------------------#
#
# Build dictionary of all subclasses of Tile
#

def FindSubclassesRec(clss):
    """Recursive function to find all subclasses of a class and return them as a list"""
    subclasses = clss.__subclasses__()
    if len(subclasses) == 0:
        return []
    else:
        results = subclasses
        for subclass in subclasses:
            results.extend(FindSubclassesRec(subclass))
        return results


tileClasses = FindSubclassesRec(Tile)
print tileClasses
tileDir = dict()
for tile in tileClasses:
    tileDir[tile.__name__] = tile

print tileDir


#-----------------------------------------------------------------------------#
#
# Engine / libtcod setup
#

PALETTE_WIDTH = 40
DATA_HEIGHT = 9

EngineSettings.FpsLimit = 2000
EngineSettings.ScreenWidth = 80+PALETTE_WIDTH
EngineSettings.ScreenHeight = 50+DATA_HEIGHT
EngineSettings.ViewWidth = 80
EngineSettings.ViewHeight = 50


# Initial libtcod setup
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.ScreenWidth, EngineSettings.ScreenHeight, 'Light test', False)
libtcod.sys_set_fps(EngineSettings.FpsLimit)


# Set renderer
renderers = {libtcod.RENDERER_GLSL: 'RENDERER_GLSL', libtcod.RENDERER_OPENGL: 'RENDERER_OPENGL',
             libtcod.RENDERER_SDL: 'RENDERER_SDL', libtcod.NB_RENDERERS: 'NB_RENDERERS'}
libtcod.sys_set_renderer(libtcod.RENDERER_OPENGL)
print "Renderer:", renderers[libtcod.sys_get_renderer()]


# Panels
paletteView = PalettePanel(None, Rect(EngineSettings.ViewWidth, 0, PALETTE_WIDTH, EngineSettings.ScreenHeight), tileDir)
dataView = LogPanel(None, Rect(0, EngineSettings.ViewHeight, EngineSettings.ViewWidth, DATA_HEIGHT-1),
                    padding=Padding(left=1, right=1, top=1, bottom=1),
                    color_data=ColorData(background_color=libtcod.sepia))

dataView.Log("NO, YOU CAN'T SAVE ANYTHING YET", libtcod.dark_cyan)
dataView.Log(".", libtcod.sepia)
dataView.Log("Mouse wheel changes brush size")
dataView.Log("Press 'B' to change brush shape")
dataView.Log("Tile palette is populated from the contents of the tiles.SimpleTiles namespace/file at the moment")

Core.init(Scene(mapW=EngineSettings.ViewWidth*2, mapH=EngineSettings.ViewHeight, ambientLight=AmbientLight(1.0), editor=True))
panels = [Core.mainWin, dataView, paletteView]

brush = Brush(Core.mainWin, paletteView)


# Editor main loop
mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    [panel.HandleInput(key, mouse) for panel in panels]
    brush.HandleInput(key, mouse)

    # start render
    libtcod.console_clear(0)  # only the printouts below actually require this. They could be shuffled into a small status bar/console of their own.
    Renderer.RenderAll(panels)

    #show FPS and coordinate of mouse cursor
    (x, y) = (mouse.cx, mouse.cy)
    libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-1,
                             libtcod.BKGND_SET, libtcod.RIGHT, '%3d FPS' % libtcod.sys_get_fps())
    libtcod.console_print_ex(None, 1, EngineSettings.ScreenHeight-1,
                             libtcod.BKGND_SET, libtcod.LEFT, 'Brush: {}, size {}'.format(brush.Shape, brush.Size))
    if Core.mainWin.Contains(x, y) and (mouse.cx, mouse.cy) != (0, 0):
        x, y = Core.mainScene.ScreenToWorldPoint(x, y)
        tileUnderCursor = Core.mainScene.GetTile(x, y)
        tileCoord = "(-, -)" if tileUnderCursor is None else tileUnderCursor.Coord
        nameUnderCursor = '-' if tileUnderCursor is None else tileUnderCursor.__class__.__name__
        libtcod.console_print_ex(None, EngineSettings.ViewWidth-2, EngineSettings.ScreenHeight-1,
                                 libtcod.BKGND_SET, libtcod.RIGHT, '{} {} {}'.format(nameUnderCursor, tileCoord, (mouse.cx, mouse.cy)))
        

    libtcod.console_flush()  # draw the console

    if key.vk == libtcod.KEY_ESCAPE:
        break
