# import libtcodpy as libtcod
# import EngineSettings
from Scene import Scene
import Audio
from gui.MainWindow import MainWindow

audio = Audio.Audio()
audio.play_music('hkblue')
mainWindow = MainWindow()
mainScene = Scene(window=mainWindow)
log = None
