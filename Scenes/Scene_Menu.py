from Scene import Scene
from Button import Button
import pygame

class Scene_Menu(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)

    def init(self):
        pygame.font.init()
        self.font = pygame.font.Font('assets/fonts/Munro.ttf', 30)
        self.playButton = Button(self.game, [32, 256], ' Start', lambda: self.game.sceneManager.setScene('Level'))

    def update(self, deltaTime, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.sceneManager.setScene('Level')
        self.playButton.update(deltaTime, events)

    def draw(self, screen):
        textSurface1 = self.font.render('press ENTER or click', False, (0, 255, 0))
        textSurface2 = self.font.render('the button to start', False, (0, 255, 0))
        screen.blit(textSurface1,(32,32))
        screen.blit(textSurface2,(32,64))
        self.playButton.draw(screen)