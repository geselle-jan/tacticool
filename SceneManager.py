import importlib

class SceneManager():
    def __init__(self, game):
        self.game = game
        self.currentSceneId = ''
        self.currentScene = None

    def getSceneClassByName(self, name):
        try:
            name = 'Scene_' + name
            sceneClass = getattr(getattr(importlib.import_module('Scenes'), name), name)
        except AttributeError:
            return None
        else:
            return sceneClass

    def setScene(self, sceneId):
        if self.currentScene != None:
            self.currentScene.destroy()
        sceneClass = self.getSceneClassByName(sceneId)
        if sceneClass != None:
            self.currentScene = sceneClass(self.game)
            self.currentSceneId = sceneId

    def update(self, deltaTime, events):
        if self.currentScene != None:
            self.currentScene.update(deltaTime, events)

    def draw(self, screen):
        if self.currentScene != None:
            self.currentScene.draw(screen)