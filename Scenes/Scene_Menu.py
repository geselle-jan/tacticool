from Scene import Scene
import pygame

class Scene_Menu(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)

    def init(self):
        pygame.font.init()
        self.font = pygame.font.Font('assets/fonts/Munro.ttf', 30)

    def update(self, deltaTime, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.sceneManager.setScene('Level')

    def draw(self, screen):
        textsurface = self.font.render('press ENTER to start', False, (0, 255, 0))
        screen.blit(textsurface,(32,32))