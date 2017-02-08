from Scene import Scene
from Map import Map
from Unit import Unit
from UI import UI
from ScrollableLayer import ScrollableLayer
import pygame

class Scene_Level(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)

    def init(self):
        self.scrollablePosition = [32,32]
        self.scrollableSize = [416,160]
        self.map = Map(self.game, 'map.tmx')
        self.game.map = self.map
        self.scrollableLayer = ScrollableLayer(self.game, self.scrollablePosition, self.scrollableSize, [0,0], self.map.size)
        self.game.scrollableLayer = self.scrollableLayer
        self.units = []
        self.units.append(Unit(self.game, [16,32]))
        self.units.append(Unit(self.game, [16,64]))
        self.units.append(Unit(self.game, [16,96]))
        self.units.append(Unit(self.game, [16,128]))
        self.ui = UI(self.game)

    def endTurn(self):
        for unit in self.units:
            unit.endTurn()

    def update(self, deltaTime, events):
        scrollSpeed = 32 * deltaTime
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or self.game.cursor.bounds['top']:
            self.scrollableLayer.changeOffsetBy([0, 1 * scrollSpeed])
        if keys[pygame.K_DOWN] or self.game.cursor.bounds['bottom']:
            self.scrollableLayer.changeOffsetBy([0, -1 * scrollSpeed])
        if keys[pygame.K_LEFT] or self.game.cursor.bounds['left']:
            self.scrollableLayer.changeOffsetBy([1 * scrollSpeed, 0])
        if keys[pygame.K_RIGHT] or self.game.cursor.bounds['right']:
            self.scrollableLayer.changeOffsetBy([-1 * scrollSpeed, 0])

        self.map.update(deltaTime, events)
        for unit in self.units:
            unit.update(deltaTime, events)
        self.scrollableLayer.update(deltaTime, events)
        self.ui.update(deltaTime, events)

    def draw(self, screen):
        self.map.draw(self.scrollableLayer.virtualSurface)
        for unit in self.units:
            unit.draw(self.scrollableLayer.virtualSurface)
        self.scrollableLayer.draw(screen)
        self.ui.draw(screen)