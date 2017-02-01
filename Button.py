from Rectangle import Rectangle

class Button():
    def __init__(self, game, position, label, function):
        self.game = game
        self.init(position, label, function)

    def init(self, position, label, function):
        self.background = Rectangle(self.game, position, [128,16], [32,32,32])

    def update(self, deltaTime, events):
        pass

    def draw(self, screen):
        self.background.draw(screen)

    def destroy(self):
        pass