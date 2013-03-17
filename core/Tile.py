from core.WObject import WObject
from gui.Helpers import ColorData
import libtcodpy as libtcod
from core import Core


class Tile(WObject):
    """Base class for a map tile"""
    def __init__(self, char, col, bgcol, x=-1, y=-1):
        super(Tile, self).__init__(x=x, y=y)
        self.Char = char
        self.ColorData = ColorData(bgcol, col, libtcod.BKGND_SET)
        self.Explored = False

    def Render(self, window):
        # TODO: should do a check for visibility and explored

        window.PaintFG(self.x, self.y, self.ColorData.foreground_color)
        window.PaintBG(self.x, self.y, self.ColorData.background_color)
        window.SetChar(self.x, self.y, self.Char)

        for obj in self.Children:
            obj.Render(window)

