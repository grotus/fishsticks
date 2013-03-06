from gui.BasePanel import BasePanel
from gui.Helpers import ColorData, Padding
from gui.Log import Log
import libtcodpy as libtcod


class LogPanel(BasePanel):
    """A message/log area"""
    def __init__(self, parent, x, y, w, h, scrollable=False, color_data=ColorData(), padding=Padding()): # scrollable is not yet supported
        super(LogPanel, self).__init__(x=x, y=y, w=w, h=h, parent=parent)
        self.log = Log(w-(padding.left+padding.right), h-(padding.top+padding.bottom), scrollable)
        self.color_data = color_data
        self.padding = padding

    def Log(self, new_msg, color = None):
        col = self.color_data.foreground_color if (color == None) else color
        self.log.Log(new_msg, col)

    def Render(self):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_background(self.console, self.color_data.background_color)

        row = self.padding.top
        for (line, color) in self.log.buffer:
            libtcod.console_set_default_foreground(self.console, color)
            libtcod.console_print_ex(self.console, self.padding.left, row, self.color_data.background_flag, libtcod.LEFT, line)
            row += 1

