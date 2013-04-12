import sys
from core.Light import AmbientLight
from core.Scene import Scene
from core.Tile import Tile
import tiles.SimpleTiles
import tiles.Nullspace
import libtcodpy as libtcod
from core import EngineSettings, Renderer, Core
from gui.LogPanel import LogPanel
from helpers.Helpers import *
from helpers import SubclassFinder
from gui.Editor import PalettePanel, EditorMapWindow, Brush
import datetime
import json


def getTimestampString():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")

MAP_SUFFIX = ".json"
filename = ""
mapdata = None
mapIsNew = True
newMapW = 100
newMapH = 100
if __name__ == '__main__':
    sys.argv.pop(0)
    if len(sys.argv) > 0:
        first = sys.argv.pop(0)
        if not first.endswith(MAP_SUFFIX):
            first += MAP_SUFFIX
        filename = first

        try:
            with open(filename) as mapsource:
                mapdata = json.load(mapsource)
                mapIsNew = False
                print "Loading map {0}, size {1}".format(filename, mapdata['dimensions'])

        except IOError, e:  # Couldn't find file, so this must be a new map
            if len(sys.argv) > 0:
                newMapW = int(sys.argv.pop(0))
            if len(sys.argv) > 0:
                newMapH = int(sys.argv.pop(0))
            print "Creating new map {0}, size {1}".format(filename, (newMapW, newMapH))

        except Exception, e:  # Scheisse!
            raise

    else:
        filename = "default"+getTimestampString()+MAP_SUFFIX
        print "Creating new map {0}, size {1}".format(filename, (newMapW, newMapH))


#-----------------------------------------------------------------------------#
#
# Build dictionary of all subclasses of Tile
#
from tiles import registry
tileDir = registry.tile_dir
print tileDir
print registry.tile_module_dir


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

dataView.Log("Press ESC to exit and saved. Clicking the X closes the window without saving.", libtcod.dark_cyan)
dataView.Log(".", libtcod.sepia)
dataView.Log("Mouse wheel changes brush size")
dataView.Log("Press 'B' to change brush shape")
dataView.Log("Tile palette is populated from the contents of the tiles.SimpleTiles namespace/file at the moment")

Core.init(Scene(mapW=newMapW, mapH=newMapH, ambientLight=AmbientLight(1.0), editor=True))
if mapdata is not None:
    w, h = mapdata['dimensions']
    tiledata = mapdata['tiledata']
    maptiles = []
    for data in tiledata:
        tileCo, clsName = data
        maptiles.append(tileDir[clsName](tileCo[0], tileCo[1]))
    Core.mainScene.SetTiles(maptiles, w, h)

panels = [Core.mainScene, dataView, paletteView]

brush = Brush(Core.mainScene.MainWindow, paletteView)


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
    if Core.mainScene.MainWindow.Contains(x, y) and (mouse.cx, mouse.cy) != (0, 0):
        x, y = Core.mainScene.ScreenToWorldPoint(x, y)
        tileUnderCursor = Core.mainScene.GetTile(x, y)
        tileCoord = "(-, -)" if tileUnderCursor is None else tileUnderCursor.Coord
        nameUnderCursor = '-' if tileUnderCursor is None else tileUnderCursor.__class__.__name__
        libtcod.console_print_ex(None, EngineSettings.ViewWidth-2, EngineSettings.ScreenHeight-1,
                                 libtcod.BKGND_SET, libtcod.RIGHT, '{} {} {}'.format(nameUnderCursor, tileCoord, (mouse.cx, mouse.cy)))

    libtcod.console_flush()  # draw the console

    if key.vk == libtcod.KEY_ESCAPE:
        scene = Core.mainScene
        mapdata = {'dimensions': (scene.Rect.w, scene.Rect.h)}
        maptiles = scene.Tiles
        tiledata = []
        for i in xrange(len(maptiles)):
            tile = maptiles[i]
            tiledata.append((tile.Coord, tile.__class__.__name__))
        mapdata['tiledata'] = tiledata
        with open(filename, 'wb') as outfile:
            json_data = json.dumps(mapdata, sort_keys=True)  # add argument indent=2 to make outputfile human-readable
            outfile.write(json_data)
            print json.loads(json_data)['dimensions']
        break
