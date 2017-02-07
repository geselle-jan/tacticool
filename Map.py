import math, pygame, pyscroll
from pytmx.util_pygame import load_pygame

class Map():
    def __init__(self, game, filename):
        self.game = game
        self.tmx_data = load_pygame('assets/maps/' + filename)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.size = [self.map_data.map_size[0] * self.map_data.tile_size[0], self.map_data.map_size[1] * self.map_data.tile_size[1]]
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.size)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

    def getTileAtPosition(self, x, y):
        layer = self.tmx_data.get_layer_by_name('collision')
        for tile in layer:
            if tile[0] is x and tile[1] is y:
                return tile[2]
        return False

    def getTileAtCoordinate(self, x, y):
        x = int(math.floor(x / 16))
        y = int(math.floor(y / 16))
        return self.getTileAtPosition(x, y)

    def draw(self, screen):
        self.group.draw(screen)

    def update(self, deltaTime, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()