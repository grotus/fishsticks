import core.Tile
import libtcodpy as libtcod


class GrassTile(core.Tile.Tile):
    def __init__(self, x, y):
        super(GrassTile, self).__init__(char='.', col=libtcod.chartreuse, bgcol=libtcod.desaturated_chartreuse, blockMove=False, blockSight=False, x=x, y=y)


class StonyGroundTile(core.Tile.Tile):
    def __init__(self, x, y):
        super(StonyGroundTile, self).__init__(char=' ', bgcol=libtcod.grey, blockMove=False, blockSight=False, x=x, y=y)


class SomeVerySpecialStoneTile(StonyGroundTile):
    def __init__(self, x, y):
        super(SomeVerySpecialStoneTile, self).__init__(x=x, y=y)


class SomeOtherStoneTile(core.Tile.Tile):
    def __init__(self, x, y):
        super(SomeOtherStoneTile, self).__init__(char=' ', bgcol=libtcod.grey, blockMove=False, blockSight=False, x=x, y=y)

