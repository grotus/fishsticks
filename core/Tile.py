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
        # TODO: should do a check for visibility and explored first

        brightness, light_col = Core.mainScene.GetIllumination(self.x, self.y)

        # libtcod.console_set_char_background(window.console, self.x, self.y, self.ColorData.background_color, self.ColorData.background_flag)
        # libtcod.console_set_char_foreground(window.console, self.x, self.y, self.ColorData.foreground_color)
        # libtcod.console_put_char(window.console, self.x, self.y, self.Char)
        libtcod.console_put_char_ex(window.console, self.x, self.y, self.Char, self.ColorData.foreground_color*brightness*light_col, self.ColorData.background_color*brightness*light_col)

        for obj in self.Children:
            obj.Render(window)

