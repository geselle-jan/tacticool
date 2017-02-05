from Rectangle import Rectangle
import pygame

class Button():
    def __init__(self, game, position, label, function):
        self.game = game
        self.init(position, label, function)

    def init(self, position, label, function):
        self.function = function
        self.position = position
        self.background = Rectangle(self.game, position, [48,16], [32,32,32])
        pygame.font.init()
        self.font = pygame.font.Font('assets/fonts/Munro.ttf', 14)
        self.textSurface = self.font.render(label, False, (255, 255, 255))

    def update(self, deltaTime, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.background.rect.collidepoint(pos):
                    self.function()

    def draw(self, screen):
        self.background.draw(screen)
        screen.blit(self.textSurface, (self.position[0] + 2, self.position[1] + 1))

    def destroy(self):
        pass