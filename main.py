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
        Rectangle.__init__(self, [16,32], [16,16], [241,241,241])
        self.movementPattern = [
                                          [ 0, -3],
                                [-1, -2], [ 0, -2], [ 1, -2],
                      [-2, -1], [-1, -1], [ 0, -1], [ 1, -1], [ 2, -1],
            [-3,  0], [-2,  0], [-1,  0],           [ 1,  0], [ 2,  0], [ 3,  0],
                      [-2,  1], [-1,  1], [ 0,  1], [ 1,  1], [ 2,  1],
                                [-1,  2], [ 0,  2], [ 1,  2],
                                          [ 0,  3],
        ]
        self.legalMovementPattern = self.movementPattern[:]
        self.showMovement = False
        self.movementRectangles = []
        for position in self.legalMovementPattern:
            realPosition = [x + y for x, y in zip(self.position, [coordinate * 16 for coordinate in position])]
            self.movementRectangles.append(
                Rectangle(realPosition, self.size, [0, 255, 0], 1)
            )

    def move(self, x, y):
        Rectangle.move(self, x, y)
        """for index, elem in enumerate(self.movementRectangles):
            self.movementRectangles[index].move(x, y)"""

    def draw(self, surface):
        Rectangle.draw(self, surface)
        if self.showMovement:
            for elem in self.movementRectangles:
                elem.draw(surface)

    def update(self):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.showMovement:
                    for movementRectangle in self.movementRectangles:
                        if movementRectangle.rect.collidepoint(pos):
                            deltaX = movementRectangle.rect.left - self.rect.left
                            deltaY = movementRectangle.rect.top - self.rect.top
                            self.move(deltaX, deltaY)
                            self.showMovement = False
                elif self.rect.collidepoint(pos):
                    unitPosition = (self.rect.left, self.rect.top)
                    self.movementRectangles = []
                    self.generateLegalMovementPattern()
                    for position in self.legalMovementPattern:
                        realPosition = [x + y for x, y in zip(unitPosition, [coordinate * 16 for coordinate in position])]
                        self.movementRectangles.append(
                            Rectangle(realPosition, self.size, [0, 255, 0], 1)
                        )
                    self.showMovement = not self.showMovement

    def checkSurrounding(self,func,x = False, y = False):
        unitPosition = (self.rect.left, self.rect.top)
        if not x:
            x = unitPosition[0]
        if not y:
            y = unitPosition[1]
        out = {}
        out["T"] = func(x     , y - 16)
        out["L"] = func(x - 16, y     )
        out["B"] = func(x     , y + 16)
        out["R"] = func(x + 16, y     )
        return out

    def isOnPlayer(self, x, y):
        return x == self.rect.left and y == self.rect.top

    def isReachable(self, x, y):
        unitPosition = (self.rect.left, self.rect.top)
        realX = int(x / 16) - int(math.floor(unitPosition[0] / 16))
        realY = int(y / 16) - int(math.floor(unitPosition[1] / 16))
        return map.getTileAtCoordinate(x, y) == 0 and [realX, realY] in self.movementPattern and not [realX, realY] in self.legalMovementPattern

    def generateLegalMovementPattern(self):
        unitPosition = (self.rect.left, self.rect.top)
        self.legalMovementPattern = []
        self.checkList = [[0, 0]]
        while self.checkList != []:
            for position in self.checkList:
                print "Baum"
                realPosition = [x + y for x, y in zip(unitPosition, [coordinate * 16 for coordinate in position])]
                self.checkDict = self.checkSurrounding(self.isReachable, realPosition[0], realPosition[1])
                print self.checkList
                print self.checkDict
                for key in self.checkDict.keys():
                    if self.checkDict[key]:
                        if key == "T":
                            self.legalMovementPattern.append([position[0], position[1]-1])
                            self.checkList.append([position[0], position[1] - 1])
                        if key == "L":
                            self.legalMovementPattern.append([position[0] -1, position[1]])
                            self.checkList.append([position[0] -1, position[1]])
                        if key == "B":
                            self.legalMovementPattern.append([position[0], position[1]+1])
                            self.checkList.append([position[0], position[1] + 1])
                        if key == "R":
                            self.legalMovementPattern.append([position[0] +1, position[1]])
                            self.checkList.append([position[0] +1, position[1]])
                self.checkList.remove(position)




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
