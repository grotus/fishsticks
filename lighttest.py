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

gamelog.Log("Lighting will be tested")

# Create some light
ambientLight = AmbientLight(col=libtcod.white, brightness=0.1)
l1 = Light(col=libtcod.red, x=20, y=20, brightness=0.9)
l2 = Light(col=libtcod.white, x=25, y=27, brightness=0.9)
Core.mainScene.AddLight(ambientLight)
Core.mainScene.AddLight(l1)
Core.mainScene.AddLight(l2)


mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    # start render
    Renderer.RenderAll(panels)
    libtcod.console_flush()  # draw the console
    # end render

    if mouse.lbutton_pressed:
        Core.mainScene.AddLight(Light(x=mouse.cx, y=mouse.cy))
    if mouse.rbutton_pressed:
        Core.mainScene.Lights.pop()

    if key.vk == libtcod.KEY_ESCAPE:
        break
