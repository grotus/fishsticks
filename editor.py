import sys
from core.Tile import Tile
import tiles.SimpleTiles
import tiles.Nullspace
import libtcodpy as libtcod
from core import EngineSettings, Renderer, Core
from gui.BasePanel import BasePanel
from gui.LogPanel import LogPanel
from helpers.Helpers import *
from gui.Editor import PalettePanel


if __name__ == '__main__':
    sys.argv.pop()
    for arg in sys.argv:
        print arg


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
DATA_HEIGHT = 10

EngineSettings.FpsLimit = 2000
EngineSettings.ScreenWidth = 80+PALETTE_WIDTH
EngineSettings.ScreenHeight = 50+DATA_HEIGHT
EngineSettings.ViewWidth = 80
EngineSettings.ViewHeight = 50

# Initial libtcod setup
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.ScreenWidth, EngineSettings.ScreenHeight, 'Light test', False)
libtcod.sys_set_fps(EngineSettings.FpsLimit)

# Panels
mapView = BasePanel(None, Rect(0, 0, EngineSettings.ViewWidth, EngineSettings.ViewHeight))
dataView = LogPanel(None, Rect(0, EngineSettings.ViewHeight, EngineSettings.ScreenWidth, DATA_HEIGHT),
                   padding=Padding(left=1, right=1, top=0, bottom=1),
                   color_data=ColorData(background_color=libtcod.sea))
paletteView = PalettePanel(None, Rect(EngineSettings.ViewWidth, 0, PALETTE_WIDTH, EngineSettings.ScreenHeight), tileDir)

panels = [mapView, dataView, paletteView]

dataView.Log("#******************#")

# Set renderer
renderers = {libtcod.RENDERER_GLSL:'RENDERER_GLSL', libtcod.RENDERER_OPENGL:'RENDERER_OPENGL',
             libtcod.RENDERER_SDL:'RENDERER_SDL', libtcod.NB_RENDERERS:'NB_RENDERERS'}
libtcod.sys_set_renderer(libtcod.RENDERER_OPENGL)
print "Renderer:", renderers[libtcod.sys_get_renderer()]

# Editor main loop
mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    paletteView.HandleInput(key, mouse)

    # start render
    Renderer.RenderAll(panels)

    #show FPS and color under mouse cursor
    (x, y) = (mouse.cx, mouse.cy)
    libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-1,
                             libtcod.BKGND_SET, libtcod.RIGHT, '%3d FPS' % libtcod.sys_get_fps())

    libtcod.console_flush()  # draw the console

    if key.vk == libtcod.KEY_ESCAPE:
        break