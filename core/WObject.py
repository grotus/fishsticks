#
# Base class for world objects (anything that's present in the world)
#
from helpers.Helpers import ColorData


class WObject(object):
    """Base class for world objects"""
    def __init__(self, x=-1, y=-1):
        self.Parent = None
        self.Children = []
        self.x = x
        self.y = y

        self.Name = "WorldObject"
        self.Desc = "A non-specific world object"

        self.Char = " "
        self.ColorData = ColorData()

    @property
    def BgCol(self):
        return self.ColorData.background_color

    @property
    def Col(self):
        return self.ColorData.foreground_color

    @property
    def BgFlag(self):
        return self.ColorData.background_flag

    @property
    def Coord(self):
        return (self.x, self.y)

    def AddChild(self, obj):
        try:
            if obj.Parent is not None:
                obj.Parent.RemoveChild(obj)

            obj.Parent = self
            self.Children.append(obj)
        except AttributeError:
            pass

    def RemoveChild(self, obj):
        try:
            self.Children.remove(obj)
            obj.Parent = None
        except ValueError:
            pass

    def Render(self, window=None):
        pass
