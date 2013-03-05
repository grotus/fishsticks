import libtcodpy as libtcod

class BasePanel(object):
    """Base class for gui panels"""
    def __init__(self, parent=None, x=0, y=0, w=80, h=50):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.console = libtcod.console_new(w, h)

        self.parent = None
        self.children = []
        if parent != None:
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
        for y in range(self.h):
            for x in range(self.w):
                libtcod.console_set_char_background(self.console, x, y, libtcod.light_chartreuse, libtcod.BKGND_SET)


class TestPanel(BasePanel):
    """just for testings"""

    def Render(self):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_foreground(self.console, libtcod.black)
        libtcod.console_set_default_background(self.console, libtcod.light_azure)
        libtcod.console_print_ex(self.console, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "Smurfing time")