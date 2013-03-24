from core import EngineSettings
from gui.BasePanel import BasePanel
from gui.MainWindow import MainWindow
from helpers.Helpers import Rect

import libtcodpy as libtcod


class PalettePanel(BasePanel):
    """docstring for PalettePanel"""
    def __init__(self, parent, rect, paletteDic):
        super(PalettePanel, self).__init__(parent, rect)
        self.Selected = None
        self.Palette = paletteDic
        self._yOff = 1
        self.Items = self.CreateItems()

        self.Dirty = True

    def Render(self):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_background(self.console, libtcod.black)
        if self.Dirty:
            self.Dirty = True

            yOff = self._yOff
            for item in self.Items.values():
                dummy = item.Dummy
                libtcod.console_put_char_ex(self.console, 1, item.y+yOff, dummy.Char, dummy.Col, dummy.BgCol)
                if item == self.Selected:
                    libtcod.console_set_default_background(self.console, libtcod.dark_amber)
                    libtcod.console_print_ex(self.console, 2, item.y+yOff, libtcod.BKGND_SCREEN, libtcod.LEFT, item.Name)
                    libtcod.console_set_default_background(self.console, libtcod.black)
                else:
                    libtcod.console_print_ex(self.console, 2, item.y+yOff, libtcod.BKGND_NONE, libtcod.LEFT, item.Name)


    def HandleInput(self, key, mouse):
        if not self.rect.Contains(mouse.cx,  mouse.cy):
            return
        if mouse.lbutton_pressed:
            clickedRow = mouse.cy
            clickedItem = self.Items.get(clickedRow, None)
            if clickedItem:
                self.Selected = clickedItem


    def CreateItems(self):
        items = dict()
        i = 0
        for obj in self.Palette:
            items[i+self._yOff] = PaletteItem(self.Palette[obj], i)
            i += 1

        if len(items.values()) > 0:
            self.Selected = items.values()[0]

        return items


class PaletteItem(object):
    def __init__(self, wobj, y):
        self.Name = wobj.__name__
        self.ItemClass = wobj
        self.Dummy = wobj(-1, -1)
        self.y = y

class EditorMapWindow(MainWindow):
    def __init__(self, rect=Rect(0, 0, EngineSettings.ViewWidth, EngineSettings.ViewHeight)):
        super(EditorMapWindow, self).__init__(rect=rect)

    def HandleInput(self, key, mouse):
        if not self.rect.Contains(mouse.cx,  mouse.cy):
            return
        if mouse.lbutton_pressed:
            print "draw at", (mouse.cx,  mouse.cy)
