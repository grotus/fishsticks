from core import EngineSettings, Renderer
from helpers.Helpers import Rect
from gui.BasePanel import BasePanel
import libtcodpy as libtcod

import array, struct
from ctypes import create_string_buffer
from libtcodpy import _lib

# Seems to perform better than libtcod's own version
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

# Seems to perform better than libtcod's own version
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
        self.ClearBuffers()


    def Render(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        while len(Renderer.TileStack) > 0:
            try:
                tile = Renderer.TileStack.pop()
                tile.Render(self)
                Renderer.LightStack.append((tile.x, tile.y))
            except Exception, e:
                raise e

        while len(Renderer.LightStack) > 0:
            try:
                x, y = Renderer.LightStack.pop()
                self.ApplyLight(x, y)
            except Exception, e:
                raise e

        # By now the RGB buffers should be filled.
        console_fill_background(self.console, self.Final_Bg_R, self.Final_Bg_G, self.Final_Bg_B)
        console_fill_foreground(self.console, self.Final_Fg_R, self.Final_Fg_G, self.Final_Fg_B)
        libtcod.console_fill_char(self.console, self.Char)

    def ApplyLight(self, x, y):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        fg_r, fg_g, fg_b = self.GetForegroundRGB(x, y)
        bg_r, bg_g, bg_b = self.GetBackgroundRGB(x, y)
        brightness = Core.mainScene.GetLightStrengthAt(x, y)
        ambient_brightness = 0 if (Core.mainScene.AmbientLight is None) else Core.mainScene.AmbientLight.Brightness

        self.Final_Fg_R[self.w * y + x] = min(int(fg_r*(brightness + ambient_brightness)), 255)
        self.Final_Fg_G[self.w * y + x] = min(int(fg_g*(brightness + ambient_brightness)), 255)
        self.Final_Fg_B[self.w * y + x] = min(int(fg_b*(brightness + ambient_brightness)), 255)

        self.Final_Bg_R[self.w * y + x] = min(int(bg_r*(brightness + ambient_brightness)), 255)
        self.Final_Bg_G[self.w * y + x] = min(int(bg_g*(brightness + ambient_brightness)), 255)
        self.Final_Bg_B[self.w * y + x] = min(int(bg_b*(brightness + ambient_brightness)), 255)


    def ApplyLightsAll(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        # Light colors
        # skipping this for now...

        # Light strength
        scene_light_map = Core.mainScene.LightMap
        ambient_brightness = 0 if (Core.mainScene.AmbientLight is None) else Core.mainScene.AmbientLight.Brightness

        self.Final_Fg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_R, scene_light_map)]
        self.Final_Fg_R = [255 if v > 255 else v for v in self.Final_Fg_R]
        self.Final_Fg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_G, scene_light_map)]
        self.Final_Fg_G = [255 if v > 255 else v for v in self.Final_Fg_G]
        self.Final_Fg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_B, scene_light_map)]
        self.Final_Fg_B = [255 if v > 255 else v for v in self.Final_Fg_B]
        self.Final_Bg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_R, scene_light_map)]
        self.Final_Bg_R = [255 if v > 255 else v for v in self.Final_Bg_R]
        self.Final_Bg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_G, scene_light_map)]
        self.Final_Bg_G = [255 if v > 255 else v for v in self.Final_Bg_G]
        self.Final_Bg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_B, scene_light_map)]
        self.Final_Bg_B = [255 if v > 255 else v for v in self.Final_Bg_B]

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

    def ClearBuffers(self):
        n = self.w * self.h
        self.Fg_R = [0] * n
        self.Fg_G = [0] * n
        self.Fg_B = [0] * n
        self.Bg_R = [0] * n
        self.Bg_G = [0] * n
        self.Bg_B = [0] * n
        self.Char = [ord(' ')] * n

        # These buffers hold the final, lit versions of the data
        self.Final_Fg_R = [0] * n
        self.Final_Fg_G = [0] * n
        self.Final_Fg_B = [0] * n
        self.Final_Bg_R = [0] * n
        self.Final_Bg_G = [0] * n
        self.Final_Bg_B = [0] * n


