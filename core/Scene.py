#
# Scene
# Stores a particular set of maptiles, lights, whatnot, that belong together.
#
from gui.MainWindow import MainWindow
from helpers.Helpers import Rect
import libtcodpy as libtcod
from tiles.Nullspace import Nullspace


class Scene(object):
    def __init__(self, window=MainWindow(), tiles=None, mapW=0, mapH=0, lights=[], ambientLight=None):
        if tiles == None:
            tiles = []
            for y in xrange(mapH):
                row = []
                for x in xrange(mapW):
                    row.append(Nullspace(x, y))
                tiles.append(row)

        self.Rect = Rect(0, 0, mapW, mapH)
        self.Tiles = self.SetTiles(tiles)
        self.PointLights = lights
        self.AmbientLight = ambientLight
        self.MainWindow = window
        self.LightMap = [0]*window.w*window.h
        self.LightColMap = [libtcod.white]*self.MainWindow.w*self.MainWindow.h


    def SetTiles(self, tiles):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.Tiles = tiles
        self.Rect = Rect(0, 0, len(tiles), len(tiles[0]))
        return self.Tiles


    def AddPointLight(self, light):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.PointLights.append(light)

    def SetAmbientLight(self, light):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.AmbientLight = light

    def CalculateLightmap(self):
        # First reset the lightmaps
        self.LightMap = [0]*self.MainWindow.w*self.MainWindow.h
        self.LightColMap = [libtcod.black]*self.MainWindow.w*self.MainWindow.h

        # Then ask each point light to add its illumination
        for light in self.PointLights:
            light.IlluminateLightmap()


    def SetLightAt(self, x, y, brightness, col=libtcod.white):
        index = self.MainWindow.w*y + x
        self.LightMap[index] = brightness
        self.LightColMap[index] = col

    def SetLightColAt(self, x, y, col):
        self.LightColMap[self.MainWindow.w*y + x] = col

    def SetLightStrengthAt(self, x, y, brightness):
        self.LightMap[self.MainWindow.w*y + x] = brightness

    def GetLightAt(self, x, y):
        index = self.MainWindow.w*y + x
        return self.LightMap[index], self.LightColMap[index]

    def GetLightColAt(self, x, y):
        return self.LightColMap[self.MainWindow.w*y + x]

    def GetLightStrengthAt(self, x, y):
        return self.LightMap[self.MainWindow.w*y + x]


