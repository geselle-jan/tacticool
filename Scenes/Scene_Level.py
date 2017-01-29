from Scene import Scene
from Map import Map
from Unit import Unit

class Scene_Level(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)

    def init(self):
        self.map = Map(self.game, 'map.tmx')
        self.game.map = self.map
        self.unit = Unit(self.game)

    def update(self, deltaTime, events):
        self.map.update(deltaTime, events)
        self.unit.update(deltaTime, events)

    def draw(self, screen):
        self.map.draw(screen)
        self.unit.draw(screen)