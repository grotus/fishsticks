# bunch of random testing
from core import EngineSettings, Renderer
from gui.BasePanel import BasePanel, TestPanel
from helpers.Helpers import Padding, ColorData, Rect
from gui.LogPanel import LogPanel
import libtcodpy as libtcod

# Initial libtcod setup...
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.ScreenWidth, EngineSettings.ScreenHeight, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(EngineSettings.FpsLimit)

# Some gui panels to test
mainpanel = BasePanel(None, Rect(0, 0, EngineSettings.ScreenWidth, EngineSettings.ScreenHeight))
subpanel = TestPanel(mainpanel, Rect(10, 10, 20, 20))

panels = [mainpanel]  # We will pass this list to the Renderer, to render the tree of panels


# Create a log area and some log messages
gamelog = LogPanel(mainpanel, Rect(0, EngineSettings.ScreenHeight-7, EngineSettings.ScreenWidth, 7),
                   padding=Padding(left=1, right=1, top=1, bottom=1),
                   color_data=ColorData(background_color=libtcod.darkest_sepia))

gamelog.Log("1: Hello world")
gamelog.Log("2: The text just keeps coming")
gamelog.Log("3: ....", libtcod.light_amber)
gamelog.Log("4: the color has changed!", libtcod.light_amber)
gamelog.Log("5: the color has changed again!", libtcod.amber)
gamelog.Log("6: Woodchuck", libtcod.dark_flame)
gamelog.Log("7: Terrible robot", libtcod.dark_flame)


mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    # start render
    Renderer.RenderAll(panels)
    libtcod.console_flush()  # draw the console
    # end render

    if key.vk == libtcod.KEY_ESCAPE:
        break
