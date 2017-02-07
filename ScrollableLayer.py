import pygame

class ScrollableLayer():
    def __init__(self, game, position, size, offset, virtualSize):
        self.game = game
        self.position = position
        self.size = size
        self.offset = offset
        self.virtualSize = virtualSize
        self.virtualSurface = pygame.Surface(self.virtualSize, pygame.SRCALPHA, 32)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)

    def changeOffsetBy(self, offset):
        self.setOffset([self.offset[0] + offset[0], self.offset[1] + offset[1]])

    def setOffset(self, offset):
        self.offset = offset
        if self.offset[0] > 0:
            self.offset[0] = 0
        if self.offset[1] > 0:
            self.offset[1] = 0
        if self.offset[0] < -1 * (self.virtualSurface.get_size()[0] - self.surface.get_size()[0]):
            self.offset[0] = -1 * (self.virtualSurface.get_size()[0] - self.surface.get_size()[0])
        if self.offset[1] < -1 * (self.virtualSurface.get_size()[1] - self.surface.get_size()[1]):
            self.offset[1] = -1 * (self.virtualSurface.get_size()[1] - self.surface.get_size()[1])

    def update(self, deltaTime, events):
        self.surface.fill((255,255,255,0))
        self.virtualSurface.fill((255,255,255,0))

    def draw(self, screen):
        self.surface.blit(self.virtualSurface, self.offset)
        screen.blit(self.surface, self.position)

    def destroy(self):
        pass