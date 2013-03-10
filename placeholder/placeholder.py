import libtcodpy as libtcod

class Placeholder(object):
    """docstring for ClassName"""
    def __init__(self):
        libtcod.console_set_custom_font('fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(80, 40, 'python/libtcod tutorial', False)

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
	
	