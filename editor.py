import sys
from core.Tile import Tile
import tiles.SimpleTiles
import tiles.Nullspace
import libtcodpy as libtcod
from core import EngineSettings, Renderer, Core


if __name__ == '__main__':
    sys.argv.pop()
    for arg in sys.argv:
        print arg


def FindSubclassesRec(clss):
    """Recursive function to find all subclasses of a class and return them as a list"""
    subclasses = clss.__subclasses__()
    if len(subclasses) == 0:
        return []
    else:
        results = subclasses
        for subclass in subclasses:
            results.extend(FindSubclassesRec(subclass))
        return results


tileClasses = FindSubclassesRec(Tile)
print tileClasses
tileDir = dict()
for tile in tileClasses:
    tileDir[tile.__name__] = tile

print tileDir

# Initial libtcod setup...
libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(EngineSettings.ScreenWidth, EngineSettings.ScreenHeight, 'Light test', False)
libtcod.sys_set_fps(EngineSettings.FpsLimit)

