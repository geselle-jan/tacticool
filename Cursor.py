import pygame, os
""" Das geht ja nich das simon mehr commits hier hat als ich,
also änder ich jetz ganz viele Dateien
-The_Lie0
"""

class Cursor(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load(os.path.join('assets', 'sprites', 'cursor.png'))
        self.rect = self.image.get_rect()
        self.centerCursor()
        pygame.mouse.set_visible(False)
        self.rect.x = self.game.width / 2
        self.rect.y = self.game.height / 2
        self.resetBounds()

    def get_pos(self):
        return [self.rect.x, self.rect.y]

    def centerCursor(self):
        pygame.mouse.set_pos(self.game.width / 2, self.game.height / 2)

    def resetBounds(self):
        self.bounds = {
            'top': False,
            'right': False,
            'bottom': False,
            'left': False
        }

    def keepInBounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > self.game.width:
            self.rect.x = self.game.width
        if self.rect.y > self.game.height:
            self.rect.y = self.game.height

    def checkBounds(self):
        self.resetBounds()
        if self.rect.x == 0:
            self.bounds['left'] = True
        if self.rect.y == 0:
            self.bounds['top'] = True
        if self.rect.x == self.game.width:
            self.bounds['right'] = True
        if self.rect.y == self.game.height:
            self.bounds['bottom'] = True

    def updatePosition(self):
        absolutePosition = pygame.mouse.get_pos()
        relativePosition = [absolutePosition[0], absolutePosition[1]]
        relativePosition[0] -= self.game.width / 2
        relativePosition[1] -= self.game.height / 2
        self.rect.x += relativePosition[0]
        self.rect.y += relativePosition[1]
        self.centerCursor()
        self.keepInBounds()
        self.checkBounds()


    def update(self, deltaTime, events):
        self.updatePosition()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
