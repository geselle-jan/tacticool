from Button import Button
import pygame, os, sys

class UI():
    def __init__(self, game):
        self.game = game
        self.init()

    def init(self):
        self.buttons = {}
        self.buttons['end_turn'] = Button(self.game, [32, 256], 'End Turn', lambda: self.game.sceneManager.currentScene.endTurn())
        self.buttons['quit'] = Button(self.game, [32, 288], 'Quit', lambda: sys.exit())
        self.background = pygame.image.load(os.path.join('assets', 'sprites', 'background.png'))
        self.backgroundRect = self.background.get_rect()
        self.backgroundRect.y = 240

    def update(self, deltaTime, events):
        for key, value in self.buttons.iteritems():
            value.update(deltaTime, events)

    def draw(self, screen):
        screen.blit(self.background, self.backgroundRect)
        for key, value in self.buttons.iteritems():
            value.draw(screen)

    def destroy(self):
        pass