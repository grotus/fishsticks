import libtcodpy as libtcod
from helpers.Helpers import Rect


class BasePanel(object):
    """Base class for gui panels"""
    def __init__(self, parent=None, rect=Rect(0, 0, 80, 50)):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h
        self.console = libtcod.console_new(rect.w, rect.h)

        self.parent = None
        self.children = []
        if parent is not None:
            parent.children.append(self)
            self.parent = parent

    def GetParent(self):
        return self.parent

    def GetChildren(self):
        return self.children

    def AddPanel(self, panel):
        self.children.append(panel)
        panel.parent = self

    def RemovePanel(self, panel):
        self.children.remove(panel)
        panel.parent = None

    def Render(self):
        """Every panel should implement their own version of Render"""
        libtcod.console_clear(self.console)
        libtcod.console_set_default_background(self.console, libtcod.light_chartreuse)


class TestPanel(BasePanel):
    """just for testings"""

    def Render(self):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_foreground(self.console, libtcod.black)
        libtcod.console_set_default_background(self.console, libtcod.light_azure)
        libtcod.console_print_ex(self.console, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "Smurfing time")
