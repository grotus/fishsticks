import libtcodpy as libtcod


class Light(object):
    """docstring for Light"""
    def __init__(self, brightness=1.0, radius=10, col=libtcod.white, x=-1, y=-1, enabled=True):
        self.Brightness = brightness
        self.__radius = radius
        self.__squared_radius = radius * radius
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

    def GetIllumination(self, x, y):
        if not self.Enabled:
            return (0.0, libtcod.white)

        # calculate squared distance to target
        r = float(self.x - x)*(self.x - x) + (self.y - y)*(self.y - y)

        if r <= self.__squared_radius:
            local_brightness = self.Brightness * float((self.__squared_radius - r) / self.__squared_radius)
            return (local_brightness, self.Col*local_brightness)
        else:
            return (0.0, libtcod.white)

class AmbientLight(object):
    def __init__(self, brightness=1.0, col=libtcod.white, enabled=True):
        self.Brightness = brightness
        self.Col = col
        self.Enabled = enabled

    def GetIllumination(self, x, y):
        if not self.Enabled:
            return (0.0, libtcod.white)

        return (self.Brightness, self.Col*self.Brightness)
