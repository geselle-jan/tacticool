import sys, pygame
import pyscroll
from pytmx.util_pygame import load_pygame
pygame.init()

size = width, height = 240, 160
black = 0, 0, 0

screen = pygame.display.set_mode(size)

tmx_data = load_pygame("map.tmx")

map_data = pyscroll.TiledMapData(tmx_data)

map_layer = pyscroll.BufferedRenderer(map_data, size)

group = pyscroll.PyscrollGroup(map_layer=map_layer)


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
        Rectangle.__init__(self, [16,16], [16,16], [255,0,0])
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)

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

    def checkSurrounding(self,func,x = False, y = False):
        if not x:
            x = self.position[0]
        if not y:
            y = self.position[1]
        out = {}
        out["UL"] = func(x - 16, y - 16)
        out["UM"] = func(x - 16, y     )
        out["UR"] = func(x - 16, y + 61)
        out["ML"] = func(x     , y - 16)
        out["MR"] = func(x     , y + 16)
        out["LL"] = func(x + 16, y - 16)
        out["LM"] = func(x + 16, y     )
        out["LR"] = func(x + 16, y + 16)
        return out


test = Unit()


while 1:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    test.update()

    screen.fill(black)

    group.draw(screen)

    test.draw(screen)

    pygame.display.flip()
