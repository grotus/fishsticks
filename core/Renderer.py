import libtcodpy as libtcod

TileStack = []  # tiles to be rendered. Might move elsewhere.
LightStack = [] # coordinates that need to be lit

def Clear():
    global TileStack, LightStack
    TileStack = []
    LightStack = []

def RenderAll(panels):
    for panel in panels:
        panel.Render()
        RenderAll(panel.children)
        if panel.parent != None:
            libtcod.console_blit(panel.console, 0, 0, panel.w, panel.h, panel.parent.console, panel.x, panel.y)
        else:
            libtcod.console_blit(panel.console, 0, 0, panel.w, panel.h, 0, panel.x, panel.y)
