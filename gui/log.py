import libtcodpy as libtcod
import textwrap

class Log(object):
    """text/message log"""
    def __init__(self, width=40, height=5, scrollable=False):
        self.width = width
        self.height = height
        self.scrollable = scrollable
        self.buffer = []

    def Log(self, new_msg, color = libtcod.white):
        #split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(new_msg, self.width)

        for line in new_msg_lines:
            #if the buffer is full, remove the first line to make room for the new one
            if not self.scrollable and len(self.buffer) == self.height:
                del self.buffer[0]

            #add the new line as a tuple, with the text and the color
            self.buffer.append( (line, color) )

    def Clear(self):
        del self.buffer[:] # clears the list