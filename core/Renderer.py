import libtcodpy as libtcod

RenderStack = []  # tiles to be rendered. Might move elsewhere.

def Clear():
    global RenderStack
    RenderStack = []

def RenderAll(panels):
    for panel in panels:
        panel.Render()
        RenderAll(panel.children)
        if panel.parent != None:
            libtcod.console_blit(panel.console, 0, 0, panel.w, panel.h, panel.parent.console, panel.x, panel.y)
        else:
            libtcod.console_blit(panel.console, 0, 0, panel.w, panel.h, 0, panel.x, panel.y)
