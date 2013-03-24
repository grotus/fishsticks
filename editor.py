import sys
from core.Tile import Tile
import tiles.SimpleTiles
import tiles.Nullspace


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