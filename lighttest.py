# bunch of random testing
from Readers.BasicAsciiReader import createTiles, testmap
from core import EngineSettings, Renderer, Core
from helpers.Helpers import Padding, ColorData, Rect
from gui.LogPanel import LogPanel
import libtcodpy as libtcod
from core.Light import Light, AmbientLight


EngineSettings.FpsLimit = 2000 # kept high for dev purposes

# Initial libtcod setup...
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.ScreenWidth, EngineSettings.ScreenHeight, 'Light test', False)
libtcod.sys_set_fps(EngineSettings.FpsLimit)

libtcod.sys_set_renderer(libtcod.RENDERER_OPENGL)

# Initialize our own engine

EngineSettings.ViewWidth = 80
EngineSettings.ViewHeight = 50-7

Core.init()

# Load testmap into the scene
testTiles, w, h = createTiles()
Core.mainScene.SetTiles(testTiles, w, h)

panels = [Core.mainScene]  # We will pass this list to the Renderer, to render the tree of panels


# Create a message log, with the mainWindow as parent
gamelog = LogPanel(Core.mainScene.MainWindow, Rect(0, EngineSettings.ScreenHeight-7, EngineSettings.ScreenWidth, 7),
                   padding=Padding(left=1, right=1, top=1, bottom=1),
                   color_data=ColorData(background_color=libtcod.darkest_sepia))
Core.logWin = gamelog

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
    if Core.mainScene.MainWindow.Contains(x, y):
        x, y = Core.mainScene.ScreenToWorldPoint(x, y)
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-4,
                                 libtcod.BKGND_SET, libtcod.RIGHT, 'Tile FG: {0}'.format(Core.mainScene.MainWindow.GetForegroundRGB(x, y)))
        libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-3,
                                 libtcod.BKGND_SET, libtcod.RIGHT, 'Tile BG: {0}'.format(Core.mainScene.MainWindow.GetBackgroundRGB(x, y)))
        libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-2,
                             libtcod.BKGND_SET, libtcod.RIGHT, 'Light: {0}'.format(Core.mainScene.GetLightAt(x, y)))
    libtcod.console_print_ex(None, EngineSettings.ScreenWidth-1, EngineSettings.ScreenHeight-1,
                             libtcod.BKGND_SET, libtcod.RIGHT, '%3d FPS' % libtcod.sys_get_fps())

    libtcod.console_flush()  # draw the console
    # end render

    if mouse.lbutton_pressed:
        Core.mainScene.AddPointLight(Light(x=mouse.cx, y=mouse.cy, col=libtcod.white, brightness=0.5))
        Core.mainScene.CalculateLightmap()
        Core.logWin.Log("New light at " + str(mouse.cx) + ", " + str(mouse.cy))
        gamelog.Log("There are {0} point lights".format(len(Core.mainScene.PointLights)))
    if mouse.rbutton_pressed:
        Core.mainScene.PointLights.pop()
        Core.mainScene.CalculateLightmap()
        gamelog.Log("There are {0} point lights".format(len(Core.mainScene.PointLights)))

    if key.c in (ord('C'), ord('c')):
        Core.mainScene.CalculateLightmap()
        Core.logWin.Log("recalculating lightmap ", color=libtcod.amber)

    if key.vk == libtcod.KEY_SPACE:
        fps = libtcod.sys_get_fps()
        Core.logWin.Log("FPS: " + str(fps), color=libtcod.amber)
        print "FPS: " + str(fps)

    if key.vk == libtcod.KEY_ESCAPE:
        break
