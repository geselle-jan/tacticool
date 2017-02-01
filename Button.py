from Rectangle import Rectangle
import pygame

class Button():
    def __init__(self, game, position, label, function):
        self.game = game
        self.init(position, label, function)

    def init(self, position, label, function):
        self.position = position
        self.background = Rectangle(self.game, position, [48,16], [32,32,32])
        pygame.font.init()
        self.font = pygame.font.Font('assets/fonts/Munro.ttf', 14)
        self.textSurface = self.font.render(label, False, (255, 255, 255))

    def update(self, deltaTime, events):
        pass

    def draw(self, screen):
        self.background.draw(screen)
        screen.blit(self.textSurface, (self.position[0] + 2, self.position[1] + 1))

    def destroy(self):
        pass