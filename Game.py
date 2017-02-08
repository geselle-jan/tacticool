import sys, pygame
from SceneManager import SceneManager
from Cursor import Cursor
""" Das geht ja nich das simon mehr commits hier hat als ich,
also änder ich jetz ganz viele Dateien
-The_Lie0
"""

class Game():
    def __init__(self):
        self.sceneManager = SceneManager(self)
        pygame.init()
        self.size = self.width, self.height = 480, 320
        self.backgroundColor = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.sceneManager.setScene('Menu')
        self.cursor = Cursor(self)
        while 1:
            deltaTime = 1 / float(self.clock.tick(60))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.update(deltaTime, events)
            self.screen.fill(self.backgroundColor)
            self.draw(self.screen)
            pygame.display.flip()

    def update(self, deltaTime, events):
        self.cursor.update(deltaTime, events)
        self.sceneManager.update(deltaTime, events)

    def draw(self, screen):
        self.sceneManager.draw(screen)
        self.cursor.draw(screen)
