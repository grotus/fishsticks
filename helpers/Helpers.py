#
# Some convenience classes, mostly struct-like in nature
#

import libtcodpy as libtcod


class Padding(object):
    """Stores padding information"""
    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class ColorData(object):
    """Stores information related to colors and blending"""
    # Adding fields to this class as I need them. Only a few for now
    def __init__(self, background_color=libtcod.black, foreground_color=libtcod.white, background_flag=libtcod.BKGND_NONE):
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.background_flag = background_flag


class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.xMin = x
        self.yMin = y
        self.xMax = x + w
        self.yMax = y + h
        self.w = w
        self.h = h

    def Center(self):
        center_x = (self.xMin + self.xMax) / 2
        center_y = (self.yMin + self.yMax) / 2
        return (center_x, center_y)

    def Intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.xMin <= other.xMax and self.xMax >= other.xMin and
                self.yMin <= other.yMax and self.yMax >= other.yMin)

    def Contains(self, x, y):
        return (self.xMin <= x and self.xMax >= x and
                self.yMin <= y and self.yMax >= y)
