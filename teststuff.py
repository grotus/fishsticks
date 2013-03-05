# bunch of random testing
from core import EngineSettings, Renderer
from gui.BasePanel import BasePanel, TestPanel
import libtcodpy as libtcod

libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.SCREEN_WIDTH, EngineSettings.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(EngineSettings.LIMIT_FPS)

mainpanel = BasePanel(None, 0, 0, EngineSettings.SCREEN_WIDTH, EngineSettings.SCREEN_HEIGHT)
subpanel = TestPanel(mainpanel, 10, 10, 20, 20)

panels = [mainpanel]

mouse = libtcod.Mouse()
key = libtcod.Key()
while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)

    # start render
    Renderer.RenderAll(panels)
    libtcod.console_flush() # draw the console
    # end render

    if key.vk == libtcod.KEY_ESCAPE:
        break

