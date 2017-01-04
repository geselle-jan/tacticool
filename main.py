import sys, math, pygame
import pyscroll
from pytmx.util_pygame import load_pygame
pygame.init()

size = width, height = 480, 320
black = 0, 0, 0

screen = pygame.display.set_mode(size)

class Rectangle():
    """A class for rectangles."""
    def __init__(self, position, size, color, stroke = 0):
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.color = color
        self.stroke = stroke

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, self.stroke)


class Unit(Rectangle):
    """A class for units."""
    def __init__(self):
        Rectangle.__init__(self, [16,16], [16,16], [241,241,241])
        self.movementPattern = [
            [0, -2],
            [-1, -1], [0, -1], [1, -1],
            [-2, 0], [-1, 0], [1, 0], [2, 0],
            [-1, 1], [0, 1], [1, 1],
            [0, 2]
        ]
        self.showMovement = False
        self.movementRectangles = []
        for position in self.movementPattern:
            realPosition = [x + y for x, y in zip(self.position, [coordinate * 16 for coordinate in position])]
            self.movementRectangles.append(
                Rectangle(realPosition, self.size, [0, 255, 0], 1)
            )

    def move(self, x, y):
        Rectangle.move(self, x, y)
        for index, elem in enumerate(self.movementRectangles):
            self.movementRectangles[index].move(x, y)

    def draw(self, surface):
        Rectangle.draw(self, surface)
        if self.showMovement:
            for elem in self.movementRectangles:
                elem.draw(surface)

    def update(self):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos):
                    self.showMovement = not self.showMovement
                if self.showMovement:
                    for movementRectangle in self.movementRectangles:
                        if movementRectangle.rect.collidepoint(pos):
                            deltaX = movementRectangle.rect.left - self.rect.left
                            deltaY = movementRectangle.rect.top - self.rect.top
                            self.move(deltaX, deltaY)
                            self.showMovement = False

class Map():
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, size)
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

    def draw(self, surface):
        self.group.draw(screen)

    def update(self):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                print map.getTileAtCoordinate(pos[0], pos[1])

map = Map('map.tmx')
unit = Unit()

while 1:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    map.update()

    unit.update()

    screen.fill(black)

    map.draw(screen)

    unit.draw(screen)

    pygame.display.flip()