from Scene import Scene
from Map import Map
from Unit import Unit
from UI import UI

class Scene_Level(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)

    def init(self):
        self.map = Map(self.game, 'map.tmx')
        self.game.map = self.map
        self.units = []
        self.units.append(Unit(self.game, [16,32]))
        self.units.append(Unit(self.game, [16,64]))
        self.units.append(Unit(self.game, [16,96]))
        self.units.append(Unit(self.game, [16,128]))
        self.ui = UI(self.game)

    def endTurn(self):
        print 'endTurn'

    def update(self, deltaTime, events):
        self.map.update(deltaTime, events)
        for unit in self.units:
            unit.update(deltaTime, events)
        self.ui.update(deltaTime, events)

    def draw(self, screen):
        self.map.draw(screen)
        for unit in self.units:
            unit.draw(screen)
        self.ui.draw(screen)