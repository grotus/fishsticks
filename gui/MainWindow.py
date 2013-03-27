from core import EngineSettings, Renderer
from helpers.Helpers import Rect
from gui.BasePanel import BasePanel
import libtcodpy as libtcod

import array, struct
from ctypes import create_string_buffer
from libtcodpy import _lib
def console_fill_background(con,r,g,b) :
##    r = array.array('i',r)
##    g = array.array('i',g)
##    b = array.array('i',b)
##    cr = r.buffer_info()[0]
##    cg = g.buffer_info()[0]
##    cb = b.buffer_info()[0]
    s = struct.Struct('%di' % len(r))
    cr = s.pack(*r)
    cg = s.pack(*g)
    cb = s.pack(*b)

    _lib.TCOD_console_fill_background(con, cr, cg, cb)

def console_fill_foreground(con,r,g,b) :
##    r = array.array('i',r)
##    g = array.array('i',g)
##    b = array.array('i',b)
##    cr = r.buffer_info()[0]
##    cg = g.buffer_info()[0]
##    cb = b.buffer_info()[0]
    s = struct.Struct('%di' % len(r))
    cr = s.pack(*r)
    cg = s.pack(*g)
    cb = s.pack(*b)

    _lib.TCOD_console_fill_foreground(con, cr, cg, cb)

class MainWindow(BasePanel):
    def __init__(self, rect=Rect(0, 0, EngineSettings.ViewWidth, EngineSettings.ViewHeight)):
        super(MainWindow, self).__init__(rect=rect)
        self.ResetBuffers()


    def Render(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        while len(Renderer.RenderStack) > 0:
            try:
                tile = Renderer.RenderStack.pop()
                tile.Render(self)
            except Exception, e:
                raise e

        # for tile in Core.mainScene.Tiles:
        #     try:
        #         tile.Render(self)
        #     except Exception, e:
        #         raise e

        # apply lights
        ((Fg_R, Fg_G, Fg_B), (Bg_R, Bg_G, Bg_B)) = self.ApplyLights()  # Get lit versions of the color buffers

        # By now the RGB buffers should be filled.
        console_fill_background(self.console, Bg_R, Bg_G, Bg_B)
        console_fill_foreground(self.console, Fg_R, Fg_G, Fg_B)
        libtcod.console_fill_char(self.console, self.Char)

    def ApplyLights(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        # Light colors
        # skipping this for now...

        # Light strength
        scene_light_map = Core.mainScene.LightMap
        ambient_brightness = 0 if (Core.mainScene.AmbientLight is None) else Core.mainScene.AmbientLight.Brightness

        Fg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_R, scene_light_map)]
        Fg_R = [255 if v > 255 else v for v in Fg_R]
        Fg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_G, scene_light_map)]
        Fg_G = [255 if v > 255 else v for v in Fg_G]
        Fg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_B, scene_light_map)]
        Fg_B = [255 if v > 255 else v for v in Fg_B]
        Bg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_R, scene_light_map)]
        Bg_R = [255 if v > 255 else v for v in Bg_R]
        Bg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_G, scene_light_map)]
        Bg_G = [255 if v > 255 else v for v in Bg_G]
        Bg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_B, scene_light_map)]
        Bg_B = [255 if v > 255 else v for v in Bg_B]
        return ((Fg_R, Fg_G, Fg_B), (Bg_R, Bg_G, Bg_B))

    def PaintBG(self, x, y, col):
        self.Bg_R[self.w * y + x] = col.r
        self.Bg_G[self.w * y + x] = col.g
        self.Bg_B[self.w * y + x] = col.b

    def PaintFG(self, x, y, col):
        self.Fg_R[self.w * y + x] = col.r
        self.Fg_G[self.w * y + x] = col.g
        self.Fg_B[self.w * y + x] = col.b

    def SetChar(self, x, y, char):
        self.Char[self.w * y + x] = ord(char)

    def GetChar(self, x, y):
        return self.Char[self.w * y + x]

    def GetForegroundRGB(self, x, y):
        return self.Fg_R[self.w * y + x], self.Fg_G[self.w * y + x], self.Fg_B[self.w * y + x]

    def GetBackgroundRGB(self, x, y):
        return self.Bg_R[self.w * y + x], self.Bg_G[self.w * y + x], self.Bg_B[self.w * y + x]

    def ResetBuffers(self):
        self.Fg_R = [0] * self.w * self.h
        self.Fg_G = [0] * self.w * self.h
        self.Fg_B = [0] * self.w * self.h
        self.Bg_R = [0] * self.w * self.h
        self.Bg_G = [0] * self.w * self.h
        self.Bg_B = [0] * self.w * self.h
        self.Char = [ord(' ')] * self.w * self.h


