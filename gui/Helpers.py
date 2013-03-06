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
