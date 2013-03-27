# import libtcodpy as libtcod
# import EngineSettings
from Scene import Scene
import Audio
from core import EngineSettings
from gui.MainWindow import MainWindow

audio = None
mainWin = None
mainScene = None
logWin = None

def init(scene=None):
    global mainWin, mainScene, logWin, audio

    mainScene = scene
    if mainScene == None:
        mainScene = Scene(mapW=EngineSettings.ViewWidth, mapH=EngineSettings.ViewHeight)
    mainWin = mainScene.MainWindow

    audio = Audio.Audio()
    #audio.play_music('hkblue')