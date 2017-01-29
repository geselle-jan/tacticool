from Rectangle import Rectangle
import pygame, math

class Unit(Rectangle):
    """A class for units."""
    def __init__(self, game):
        self.game = game
        Rectangle.__init__(self, self.game, [16,32], [16,16], [241,241,241])
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
                Rectangle(self.game, realPosition, self.size, [0, 255, 0], 1)
            )

    def move(self, x, y):
        Rectangle.move(self, x, y)
        """for index, elem in enumerate(self.movementRectangles):
            self.movementRectangles[index].move(x, y)"""

    def draw(self, screen):
        Rectangle.draw(self, screen)
        if self.showMovement:
            for elem in self.movementRectangles:
                elem.draw(screen)

    def update(self, deltaTime, events):
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
                            Rectangle(self.game, realPosition, self.size, [0, 255, 0], 1)
                        )
                    self.showMovement = not self.showMovement

    def checkSurrounding(self,func,x = "NIX", y = "NIX", extralist = False, multiplier = 16):
        unitPosition = (self.rect.left, self.rect.top)
        if x == "NIX":
            x = unitPosition[0]
        if y == "NIX":
            y = unitPosition[1]
        out = {}
        if extralist:
            out["T"] = func(x             , y - multiplier, extralist)
            out["L"] = func(x - multiplier, y             , extralist)
            out["B"] = func(x             , y + multiplier, extralist)
            out["R"] = func(x + multiplier, y             , extralist)
        else:
            out["T"] = func(x             , y - multiplier)
            out["L"] = func(x - multiplier, y             )
            out["B"] = func(x             , y + multiplier)
            out["R"] = func(x + multiplier, y             )
        return out

    def isOnPlayer(self, x, y):
        return x == self.rect.left and y == self.rect.top

    def isReachable(self, x, y):
        unitPosition = (self.rect.left, self.rect.top)
        realX = int(x / 16) - int(math.floor(unitPosition[0] / 16))
        realY = int(y / 16) - int(math.floor(unitPosition[1] / 16))
        return self.game.map.getTileAtCoordinate(x, y) == 0 and [realX, realY] in self.movementPattern and not [realX, realY] in self.legalMovementPattern

    def generateLegalMovementPattern(self):
        unitPosition = (self.rect.left, self.rect.top)
        self.legalMovementPattern = []
        self.checkList = [[0, 0]]
        while self.checkList != []:
            for position in self.checkList:
                realPosition = [x + y for x, y in zip(unitPosition, [coordinate * 16 for coordinate in position])]
                self.checkDict = self.checkSurrounding(self.isReachable, realPosition[0], realPosition[1])
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

    def girlScout(self, doSiDos):
        thinMints = []
        shortBreadSlashTrefoils = self.getScore(0,0,doSiDos)
        eternalScout = {shortBreadSlashTrefoils:[[0,0]]}
        toffeeTastic = True
        while toffeeTastic:
            trios = eternalScout.keys()[0]
            for score in eternalScout.keys():
                if score < trios:
                    trios = score
            position = eternalScout.setdefault(trios, [[0,0]])[-1]
            if not position in thinMints:
                caramelDeLites = self.checkSurrounding(self.getScore, position[0], position[1], doSiDos, 1)
                for path in caramelDeLites.keys():
                        if caramelDeLites[path]:
                            if path == "T":
                                eternalScout[caramelDeLites[path]] = eternalScout[trios] + [[position[0], position[1] - 1]]
                            if path == "L":
                                eternalScout[caramelDeLites[path]] = eternalScout[trios] + [[position[0] - 1, position[1]]]
                            if path == "B":
                                eternalScout[caramelDeLites[path]] = eternalScout[trios] + [[position[0], position[1] + 1]]
                            if path == "R":
                                eternalScout[caramelDeLites[path]] = eternalScout[trios] + [[position[0] + 1, position[1]]]
            del eternalScout[trios]
            thinMints.append(position)
            for key in eternalScout.keys():
                if doSiDos in eternalScout[key]:
                    toffeeTastic = False
                    return eternalScout[key]
            if eternalScout == {}:
                return False

    def getScore(self, x, y, destination):
        if [x,y] in self.legalMovementPattern or [x,y] == [0,0]:
            return abs(math.sqrt(x**2+y**2)) + abs(math.sqrt((destination[0]-x)**2+(destination[1]-y)**2))
        else:
            return False