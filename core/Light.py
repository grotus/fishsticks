from helpers.Helpers import Rect
import libtcodpy as libtcod
from core import Core


class Light(object):
    """docstring for Light"""

    def __init__(self, brightness=1.0, radius=10, col=libtcod.white, x=-1, y=-1, enabled=True):
        self.Brightness = brightness
        self.__radius = radius
        self.__squared_radius = radius * radius
        self.__bounds = Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.Col = col
        self.x = x
        self.y = y
        self.Enabled = enabled

    @property
    def Radius(self):
        return self.__radius

    @Radius.setter
    def Radius(self, value):
        self.__radius = value
        self.__squared_radius = value * value

    @property
    def Bounds(self):
        return self.__bounds

    def IlluminateLightmap(self):
        bounds = self.__bounds
        for y in range(bounds.yMin, bounds.yMax):
            for x in range(bounds.xMin, bounds.xMax):
                # calculate squared distance to target
                r = float(self.x - x) * (self.x - x) + (self.y - y) * (self.y - y)
                if r <= self.__squared_radius:
                    local_brightness = self.Brightness * float((self.__squared_radius - r) / self.__squared_radius)
                    lightmap_bright, lightmap_col = Core.mainScene.GetLightAt(x, y)
                    Core.mainScene.SetLightAt(x, y, lightmap_bright + local_brightness, lightmap_col + self.Col)

    #deprecated
    def GetIllumination(self, x, y):
        if not self.Enabled:
            return (0.0, libtcod.white)

        # calculate squared distance to target
        r = float(self.x - x) * (self.x - x) + (self.y - y) * (self.y - y)

        if r <= self.__squared_radius:
            local_brightness = self.Brightness * float((self.__squared_radius - r) / self.__squared_radius)
            return self.Col * local_brightness
            #return (local_brightness, self.Col*local_brightness)
        else:
            return libtcod.black
            #return (0.0, libtcod.white)


class AmbientLight(object):
    def __init__(self, brightness=1.0, col=libtcod.white, enabled=True):
        self.Brightness = brightness
        self.Col = col
        self.Enabled = enabled

    def GetIllumination(self, x, y):
        if not self.Enabled:
            return (0.0, libtcod.white)

        return (self.Brightness, self.Col * self.Brightness)
