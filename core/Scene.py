#
# Scene
# Stores a particular set of maptiles, lights, whatnot, that belong together.
#
from gui.MainWindow import MainWindow
from helpers.Helpers import Rect
import libtcodpy as libtcod
from tiles.Nullspace import Nullspace
from core import Renderer
from gui.Editor import EditorMapWindow


class Scene(object):
    def __init__(self, mapW=0, mapH=0, lights=[], ambientLight=None, editor=False):

        Renderer.Clear()
        tiles = []
        for y in xrange(mapH):
            for x in xrange(mapW):
                tiles.append(Nullspace(x, y))

        self.Rect = None  # Assigned with the SetTiles call
        self.Tiles = None
        self.LightMap = None
        self.LightColMap = None
        self.SetTiles(tiles, mapW, mapH)

        self.PointLights = lights
        self.AmbientLight = ambientLight
        self.MainWindow = None
        if not editor:
            self.MainWindow = MainWindow(self)
        else:
            self.MainWindow = EditorMapWindow(self)

    def Contains(self, x, y):
        return self.Rect.Contains(x, y)

    def SetTiles(self, tiles, w, h):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        if len(tiles) != w*h:
            raise Exception('Specified dimensions does not match size of tile list')

        Renderer.Clear()  # Should perhaps only purge the tilestack? This step is probably redundant.
        Renderer.TileStack = list(tiles)  # render aLL these tiles. It's vital that we copy the list rather than assign it directly. 
        self.Tiles = tiles
        self.Rect = Rect(0, 0, w, h)
        self.LightMap = [0]*w*h
        self.LightColMap = [libtcod.white]*w*h

    def GetTile(self, x, y):
        if not self.Rect.Contains(x, y):
            return None
        return self.Tiles[self.Rect.w*y+x]

    def SetTile(self, x, y, tile):
        if self.Rect.Contains(x, y):
            self.Tiles[self.Rect.w*y+x] = tile

    def AddPointLight(self, light):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.PointLights.append(light)

    def SetAmbientLight(self, light):
        # Might change this to create the light, rather than just be a wrapper for appending to a list
        self.AmbientLight = light

    def CalculateLightmap(self):
        # First reset the lightmaps
        self.LightMap = [0]*self.Rect.w*self.Rect.h
        self.LightColMap = [libtcod.black]*self.Rect.w*self.Rect.h

        # Then ask each point light to add its illumination
        for light in self.PointLights:
            light.IlluminateLightmap()

    def SetLightAt(self, x, y, brightness, col=libtcod.white):
        index = self.Rect.w*y + x
        self.LightMap[index] = brightness
        self.LightColMap[index] = col

    def SetLightColAt(self, x, y, col):
        self.LightColMap[self.Rect.w*y + x] = col

    def SetLightStrengthAt(self, x, y, brightness):
        self.LightMap[self.Rect.w*y + x] = brightness

    def GetLightAt(self, x, y):
        index = self.Rect.w*y + x
        return self.LightMap[index], self.LightColMap[index]

    def GetLightColAt(self, x, y):
        return self.LightColMap[self.Rect.w*y + x]

    def GetLightStrengthAt(self, x, y):
        return self.LightMap[self.Rect.w*y + x]

    def ScreenToWorldPoint(self, x, y):
        offx, offy = self.MainWindow.Focus
        return offx+x, offy+y
