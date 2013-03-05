import libtcodpy as libtcod
import textwrap

LOG_WIDTH = 40
LOG_HEIGHT = 5
msg_buffer = ["hurr"]

# TODO: Change this so there's a scrollable log history?
def log(new_msg, color = libtcod.white):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, LOG_WIDTH)

    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(msg_buffer) == LOG_HEIGHT:
            del msg_buffer[0]

        #add the new line as a tuple, with the text and the color
        msg_buffer.append( (line, color) )

def clear():
    msg_buffer = []