#
# Scene
# Stores a particular set of maptiles, lights, whatnot, that belong together.
#
import libtcodpy as libtcod

class Scene(object):
    def __init__(self, tiles=[], lights=[], window=None):
        self.Map = tiles
        self.Lights = lights
        self.MainWindow = window

    def AddLight(self, light):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.Lights.append(light)

    def GetIllumination(self, x, y):
        brightness = 0.0
        col = libtcod.white
        from core import Core
        for light in Core.mainScene.Lights:
            b, c = light.GetIllumination(x, y)
            brightness += b
            col += c

        return (brightness, col)
