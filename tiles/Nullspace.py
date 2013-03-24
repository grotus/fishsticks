import core.Tile
from helpers.Helpers import ColorData
import libtcodpy as libtcod

class Nullspace(core.Tile.Tile):
    def __init__(self, x, y):
        super(Nullspace, self).__init__(x=x, y=y)
        self.Char = '?'
        self.ColorData = ColorData(libtcod.black, libtcod.dark_gray, libtcod.BKGND_SET)
        self.Explored = False
