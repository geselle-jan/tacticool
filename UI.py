from Button import Button
import pygame, os

class UI():
    def __init__(self, game):
        self.game = game
        self.init()

    def init(self):
        self.buttons = {}
        self.buttons['end_turn'] = Button(self.game, [32, 256], 'End Turn', lambda: self.game.sceneManager.currentScene.endTurn())
        self.background = pygame.image.load(os.path.join('assets', 'sprites', 'frame.png'))

    def update(self, deltaTime, events):
        for key, value in self.buttons.iteritems():
            value.update(deltaTime, events)

    def draw(self, screen):
        screen.blit(self.background, self.background.get_rect())
        for key, value in self.buttons.iteritems():
            value.draw(screen)

    def destroy(self):
        pass