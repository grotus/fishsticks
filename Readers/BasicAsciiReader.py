#
# At the moment, this one is just for a quick test
# Turns ascii into Tiles
#

import libtcodpy as libtcod
from core.Tile import Tile

testmap = """
........;;;;;;;;;;;...........................;;;;;;;;;;;........;;;;;;;;;;;........;;;;;;;;;;;
..........;;;;;;;;;.............................;;;;;;;;;..........;;;;;;;;;..........;;;;;;;;;
..............;;;;;.................................;;;;;..............;;;;;..............;;;;;
...............;;;;..................................;;;;...............;;;;...............;;;;
........#......;;;;...........................#......;;;;........#......;;;;........#......;;;;
........#........;;.......###.................#........;;........#........;;........#........;;
....#####...............T....#............#####..............#####..............#####..........
..T..........................###........T..................T..................T................
......................T........................................................................
..T........................T............T..................T..................T................
........T............T........................T..................T..................T..........
...T.....................................T..................T..................T...............
..........###........T..........................###................###................###......
.....T....#............#####...............T....#.............T....#.............T....#........
.......###.................#........;;.......###................###................###.........
...........................#......;;;;.........................................................
..................................;;;;.........................................................
.................................;;;;;.........................................................
.............................;;;;;;;;;.........................................................
...........................;;;;;;;;;;;.........................................................
...........................;;;;;;;;;;;........;;;;;;;;;;;........;;;;;;;;;;;........;;;;;;;;;;;
.............................;;;;;;;;;..........;;;;;;;;;..........;;;;;;;;;..........;;;;;;;;;
.................................;;;;;..............;;;;;..............;;;;;..............;;;;;
..................................;;;;...............;;;;...............;;;;...............;;;;
...........................#......;;;;........#......;;;;........#......;;;;........#......;;;;
.......###.................#........;;........#........;;........#........;;........#........;;
.....T....#............#####..............#####..............#####..............#####..........
..........###........T..................T..................T..................T................
...T...........................................................................................
........T............T..................T..................T..................T................
..T........................T..................T..................T..................T..........
......................T..................T..................T..................T...............
..T..........................###................###................###................###......
....#####...............T....#.............T....#.............T....#.............T....#........
........#........;;.......###................###................###................###.........
........#......;;;;............................................................................
...............;;;;............................................................................
..............;;;;;............................................................................
..........;;;;;;;;;............................................................................
........;;;;;;;;;;;............................................................................
...............;;;;............................................................................
..............;;;;;............................................................................
..........;;;;;;;;;............................................................................
........;;;;;;;;;;;............................................................................
""".strip().split()



def createTiles(mapstring):
    """Returns a matrix of map tiles"""
    map = []
    x, y = 0, 0
    for row in testmap:
        maprow = []
        map.append(maprow)
        for char in row:
            maprow.append(makeTile(char, x, y))
            x += 1
        y += 1
        x = 0

    return map


def makeTile(char, x, y):
    col, bgcol = libtcod.white, libtcod.black
    if char == '.':
        col, bgcol = libtcod.chartreuse, libtcod.desaturated_chartreuse
        char = ' '
    elif char == ';':
        col, bgcol = libtcod.dark_chartreuse, libtcod.darker_chartreuse
        char = ' '
    elif char == 'T':
        col, bgcol = libtcod.dark_orange, libtcod.desaturated_chartreuse
    elif char == '#':
        col, bgcol = libtcod.dark_grey, libtcod.desaturated_chartreuse


    return Tile(char, col, bgcol, x, y)
