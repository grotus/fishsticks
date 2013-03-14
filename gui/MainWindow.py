from core import EngineSettings
from gui.Helpers import Rect
from gui.BasePanel import BasePanel

class MainWindow(BasePanel):
    def __init__(self, rect=Rect(0, 0, EngineSettings.MAIN_WIDTH, EngineSettings.MAIN_HEIGHT)):
        super(MainWindow, self).__init__(rect=rect)

    def Render(self):
        from core import Core  # importing here to circumvent an annoying circular import dependency

        for row in Core.mainScene.Map:
            for tile in row:
                try:
                    tile.Render(self)
                except Exception, e:
                    raise e
                
