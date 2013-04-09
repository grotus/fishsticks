from core.Tile import Tile
from helpers import SubclassFinder

tile_list = SubclassFinder.FindSubclassesRec(Tile)

tile_dir = dict()
tile_module_dir = dict()

for tile in tile_list:
    tile_dir[tile.__name__] = tile
    tile_module_dir[(tile.__module__, tile.__name__)] = tile
