from core.WObject import WObject
from helpers.Helpers import ColorData
import libtcodpy as libtcod


class Tile(WObject):
    """Base class for a map tile"""
    def __init__(self, char='.', col=libtcod.white, bgcol=libtcod.black, x=-1, y=-1, blockMove=False, blockSight=False):
        super(Tile, self).__init__(x=x, y=y)
        self.Char = char
        self.ColorData = ColorData(bgcol, col, libtcod.BKGND_SET)
        self.Explored = False
        self.BlockMove = blockMove
        self.BlockSight = blockSight
        self.IsDirty = True  # Determines if the tile should be re-drawn

    def Render(self, window):
        # TODO: should do a check for visibility and explored

        if self.IsDirty:
            window.PaintFG(self.x, self.y, self.ColorData.foreground_color)
            window.PaintBG(self.x, self.y, self.ColorData.background_color)
            window.SetChar(self.x, self.y, self.Char)
            self.IsDirty = False

        for obj in self.Children:
            obj.Render(window)

