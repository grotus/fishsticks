from core import EngineSettings
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

        #Core.mainScene.CalculateLightmap()

        for tile in Core.mainScene.Tiles:
            try:
                tile.Render(self)
            except Exception, e:
                raise e

        # apply lights
        self.ApplyLights()

        # By now the RGB buffers should be filled.
        console_fill_background(self.console, self.Bg_R, self.Bg_G, self.Bg_B)
        console_fill_foreground(self.console, self.Fg_R, self.Fg_G, self.Fg_B)
        libtcod.console_fill_char(self.console, self.Char)

    def ApplyLights(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        # Light colors
        # self.Fg_R = [v*c.r for v, c in zip(self.Fg_R, Core.mainScene.LightColMap)]
        # self.Fg_G = [v*c.g for v, c in zip(self.Fg_G, Core.mainScene.LightColMap)]
        # self.Fg_B = [v*c.b for v, c in zip(self.Fg_B, Core.mainScene.LightColMap)]
        # self.Bg_R = [v*c.r/255.0 for v, c in zip(self.Bg_R, Core.mainScene.LightColMap)]
        # self.Bg_G = [v*c.g/255.0 for v, c in zip(self.Bg_G, Core.mainScene.LightColMap)]
        # self.Bg_B = [v*c.b/255.0 for v, c in zip(self.Bg_B, Core.mainScene.LightColMap)]

        # Light strength
        scene_light_map = Core.mainScene.LightMap
        ambient_brightness = 0 if (Core.mainScene.AmbientLight==None) else Core.mainScene.AmbientLight.Brightness
        self.Fg_R = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Fg_R, scene_light_map)]
        self.Fg_G = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Fg_G, scene_light_map)]
        self.Fg_B = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Fg_B, scene_light_map)]
        self.Bg_R = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Bg_R, scene_light_map)]
        self.Bg_G = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Bg_G, scene_light_map)]
        self.Bg_B = [int(min(v*(s + ambient_brightness), 255)) for v, s in zip(self.Bg_B, scene_light_map)]

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


