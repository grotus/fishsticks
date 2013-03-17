# bunch of random testing
from Readers.BasicAsciiReader import createTiles, testmap
from core import EngineSettings, Renderer, Core
from gui.Helpers import Padding, ColorData, Rect
from gui.LogPanel import LogPanel
import libtcodpy as libtcod
from core.Light import Light, AmbientLight


# Initial libtcod setup...
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.SCREEN_WIDTH, EngineSettings.SCREEN_HEIGHT, 'Light test', False)
libtcod.sys_set_fps(EngineSettings.LIMIT_FPS)

# Load testmap into the scene
Core.mainScene.Map = createTiles(testmap)

panels = [Core.mainWindow]  # We will pass this list to the Renderer, to render the tree of panels


# Create a message log, with the mainWindow as parent
gamelog = LogPanel(Core.mainWindow, Rect(0, EngineSettings.SCREEN_HEIGHT-7, EngineSettings.SCREEN_WIDTH, 7),
                   padding=Padding(left=1, right=1, top=1, bottom=1),
                   color_data=ColorData(background_color=libtcod.darkest_sepia))
Core.log = gamelog

# Create some light
ambientLight = AmbientLight(col=libtcod.white, brightness=0.15)
l1 = Light(col=libtcod.red, x=20, y=20, brightness=0.9)
l2 = Light(col=libtcod.lightest_yellow, x=25, y=27, brightness=0.9)
Core.mainScene.SetAmbientLight(ambientLight)
Core.mainScene.AddPointLight(l1)
Core.mainScene.AddPointLight(l2)

Core.mainScene.CalculateLightmap()

gamelog.Log("Lighting will be tested")
gamelog.Log("There are {0} point lights".format(len(Core.mainScene.PointLights)))
testcol = libtcod.white * libtcod.yellow
gamelog.Log("Color: {}".format(testcol))

mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    # start render
    Renderer.RenderAll(panels)

    #show FPS and color under mouse cursor
    (x, y) = (mouse.cx, mouse.cy)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print_ex(None, EngineSettings.SCREEN_WIDTH-1, EngineSettings.SCREEN_HEIGHT-4,
                             libtcod.BKGND_SET, libtcod.RIGHT, 'Tile FG: {0}'.format(Core.mainWindow.GetForegroundRGB(x, y)))
    libtcod.console_print_ex(None, EngineSettings.SCREEN_WIDTH-1, EngineSettings.SCREEN_HEIGHT-3,
                             libtcod.BKGND_SET, libtcod.RIGHT, 'Tile BG: {0}'.format(Core.mainWindow.GetBackgroundRGB(x, y)))
    libtcod.console_print_ex(None, EngineSettings.SCREEN_WIDTH-1, EngineSettings.SCREEN_HEIGHT-2,
                         libtcod.BKGND_SET, libtcod.RIGHT, 'Light: {0}'.format(Core.mainScene.GetLightAt(x, y)))
    libtcod.console_print_ex(None, EngineSettings.SCREEN_WIDTH-1, EngineSettings.SCREEN_HEIGHT-1,
                             libtcod.BKGND_SET, libtcod.RIGHT, '%3d FPS' % libtcod.sys_get_fps())

    libtcod.console_flush()  # draw the console
    # end render

    if mouse.lbutton_pressed:
        Core.mainScene.AddPointLight(Light(x=mouse.cx, y=mouse.cy, col=libtcod.white, brightness=0.5))
        Core.mainScene.CalculateLightmap()
        Core.log.Log("New light at " + str(mouse.cx) + ", " + str(mouse.cy))
        gamelog.Log("There are {0} point lights".format(len(Core.mainScene.PointLights)))
    if mouse.rbutton_pressed:
        Core.mainScene.PointLights.pop()
        Core.mainScene.CalculateLightmap()
        gamelog.Log("There are {0} point lights".format(len(Core.mainScene.PointLights)))

    if key.c in (ord('C'), ord('c')):
        Core.mainScene.CalculateLightmap()
        Core.log.Log("recalculating lightmap ", color=libtcod.amber)

    if key.vk == libtcod.KEY_SPACE:
        fps = libtcod.sys_get_fps()
        Core.log.Log("FPS: " + str(fps), color=libtcod.amber)
        print "FPS: " + str(fps)

    if key.vk == libtcod.KEY_ESCAPE:
        break
