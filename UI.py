from Button import Button

class UI():
    def __init__(self, game):
        self.game = game
        self.init()

    def init(self):
        self.buttons = {}
        self.buttons['end_turn'] = Button(self.game, [0, 0], 'End Turn', lambda: self.game.sceneManager.currentScene.endTurn())

    def update(self, deltaTime, events):
        for key, value in self.buttons.iteritems():
            value.update(deltaTime, events)

    def draw(self, screen):
        for key, value in self.buttons.iteritems():
            value.draw(screen)

    def destroy(self):
        pass