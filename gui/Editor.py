from core import EngineSettings, Core
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
    def __init__(self, palette, rect):
        super(EditorMapWindow, self).__init__(rect=rect)

    def HandleInput(self, key, mouse):
        if not self.rect.Contains(mouse.cx,  mouse.cy):
            return
        pass


class Brush(object):
    """docstring for Brush"""
    def __init__(self, canvas, palette):
        super(Brush, self).__init__()
        self.Canvas = canvas
        self.Palette = palette
        self.Size = 1

        self.__lastX = -1
        self.__lastY = -1


    def HandleInput(self, key, mouse):
        if not self.Canvas.rect.Contains(mouse.cx,  mouse.cy):
            return

        if (mouse.dcx, mouse.dcy) != (0, 0):
            self.__lastX, self.__lastY = -1, -1

        if mouse.lbutton and (mouse.cx, mouse.cy) != (self.__lastX, self.__lastY):
            self.__lastX, self.__lastY = mouse.cx, mouse.cy
            mapX, mapY = mouse.cx, mouse.cy # will need to translate this later, to account for map scrolling
            self.Paint(mapX, mapY)

        if mouse.wheel_up:
            self.Size = min(self.Size + 1, 10)
            print "Brush size", self.Size
        if mouse.wheel_down:
            self.Size = max(self.Size - 1, 1)
            print "Brush size", self.Size

    def Paint(self, x, y):
        brush = self.Palette.Selected
        size = self.Size - 1
        for py in xrange(y-size, y+size+1):
            for px in xrange(x-size, x+size+1):
                if Core.mainScene.Contains(px, py) and\
                        (not Core.mainScene.GetTile(px, py).__class__ == brush.ItemClass):
                    #print "draw", brush.Name, "at", (mouse.cx,  mouse.cy)
                    Core.mainScene.SetTile(px, py, brush.ItemClass(px, py))