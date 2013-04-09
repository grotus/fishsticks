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
    def __init__(self, scene):
        super(MainWindow, self).__init__(rect=Rect(0, 0, EngineSettings.ViewWidth, EngineSettings.ViewHeight))
        self.Scene = scene
        self.ClearBuffers()
        self.Focus = (0, 0)
        self.__MapConsole = libtcod.console_new(self.Scene.Rect.w, self.Scene.Rect.h)

    def Render(self):
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

        console_fill_background(self.__MapConsole, self.Final_Bg_R, self.Final_Bg_G, self.Final_Bg_B)
        console_fill_foreground(self.__MapConsole, self.Final_Fg_R, self.Final_Fg_G, self.Final_Fg_B)
        libtcod.console_fill_char(self.__MapConsole, self.Char)
        libtcod.console_clear(self.console)
        camX, camY = self.Focus
        libtcod.console_blit(self.__MapConsole, camX, camY, EngineSettings.ViewWidth, EngineSettings.ViewHeight, self.console, 0, 0)

    def ApplyLight(self, x, y):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        fg_r, fg_g, fg_b = self.GetForegroundRGB(x, y)
        bg_r, bg_g, bg_b = self.GetBackgroundRGB(x, y)
        brightness = Core.mainScene.GetLightStrengthAt(x, y)
        ambient_brightness = 0 if (Core.mainScene.AmbientLight is None) else Core.mainScene.AmbientLight.Brightness

        mapWidth = self.Scene.Rect.w
        self.Final_Fg_R[mapWidth * y + x] = min(int(fg_r*(brightness + ambient_brightness)), 255)
        self.Final_Fg_G[mapWidth * y + x] = min(int(fg_g*(brightness + ambient_brightness)), 255)
        self.Final_Fg_B[mapWidth * y + x] = min(int(fg_b*(brightness + ambient_brightness)), 255)

        self.Final_Bg_R[mapWidth * y + x] = min(int(bg_r*(brightness + ambient_brightness)), 255)
        self.Final_Bg_G[mapWidth * y + x] = min(int(bg_g*(brightness + ambient_brightness)), 255)
        self.Final_Bg_B[mapWidth * y + x] = min(int(bg_b*(brightness + ambient_brightness)), 255)


    # Deprecate?
    # def ApplyLightsAll(self):
    #     from core import Core  # importing here to circumvent an annoying circular import dependency

    #     # Light colors
    #     # skipping this for now...

    #     # Light strength
    #     scene_light_map = Core.mainScene.LightMap
    #     ambient_brightness = 0 if (Core.mainScene.AmbientLight is None) else Core.mainScene.AmbientLight.Brightness

    #     self.Final_Fg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_R, scene_light_map)]
    #     self.Final_Fg_R = [255 if v > 255 else v for v in self.Final_Fg_R]
    #     self.Final_Fg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_G, scene_light_map)]
    #     self.Final_Fg_G = [255 if v > 255 else v for v in self.Final_Fg_G]
    #     self.Final_Fg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Fg_B, scene_light_map)]
    #     self.Final_Fg_B = [255 if v > 255 else v for v in self.Final_Fg_B]
    #     self.Final_Bg_R = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_R, scene_light_map)]
    #     self.Final_Bg_R = [255 if v > 255 else v for v in self.Final_Bg_R]
    #     self.Final_Bg_G = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_G, scene_light_map)]
    #     self.Final_Bg_G = [255 if v > 255 else v for v in self.Final_Bg_G]
    #     self.Final_Bg_B = [int(v*(l + ambient_brightness)) for v, l in zip(self.Bg_B, scene_light_map)]
    #     self.Final_Bg_B = [255 if v > 255 else v for v in self.Final_Bg_B]

    def PaintBG(self, x, y, col):
        mapWidth = self.Scene.Rect.w
        self.Bg_R[mapWidth * y + x] = col.r
        self.Bg_G[mapWidth * y + x] = col.g
        self.Bg_B[mapWidth * y + x] = col.b

    def PaintFG(self, x, y, col):
        mapWidth = self.Scene.Rect.w
        self.Fg_R[mapWidth * y + x] = col.r
        self.Fg_G[mapWidth * y + x] = col.g
        self.Fg_B[mapWidth * y + x] = col.b

    def SetChar(self, x, y, char):
        self.Char[self.Scene.Rect.w * y + x] = ord(char)

    def GetChar(self, x, y):
        return self.Char[self.Scene.Rect.w * y + x]

    def GetForegroundRGB(self, x, y):
        mapWidth = self.Scene.Rect.w
        return self.Fg_R[mapWidth * y + x], self.Fg_G[mapWidth * y + x], self.Fg_B[mapWidth * y + x]

    def GetBackgroundRGB(self, x, y):
        mapWidth = self.Scene.Rect.w
        return self.Bg_R[mapWidth * y + x], self.Bg_G[mapWidth * y + x], self.Bg_B[mapWidth * y + x]

    def ClearBuffers(self):
        n = self.Scene.Rect.w * self.Scene.Rect.h
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


